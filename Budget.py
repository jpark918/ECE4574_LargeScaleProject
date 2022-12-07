from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5 import QtWidgets, QtCore
from datetime import date
from PyQt5 import uic
from PyQt5.Qt import Qt
import random
import pymysql

/*
 *	Budget.py  Atta-Boakye, Park, Shoaib  Virginia Tech  Dec. 7, 2022
 *	
 *	This is the main executable script file that is to be run on a local terminal.
 *	This file connects to the database where user data/information is stored.
 * 	The file then displays user data on the default executable page with a graph displaying
 *	the total budget spent/available during the current month.
 *  User interaction allows them to view different 'pages' and view different graphs such as
 *  subscription/expenses.
 *	For the purpose of this project, Shoaib's web subscription data has been monitored and 
 * 	used.
 *	Shoaib has contributed with data retrieval and GUI
 *	Atta-Boakye has contributed with the database and GUI and data access
 *	Park has contributed with the GUI and Graphs and data access
 */


months_map = {"01":"January",
            "02":"February",
            "03":"March",
            "04":"April",
            "05":"May",
            "06":"June",
            "07":"July",
            "08":"August",
            "09": "September",
            "10" : "October",
            "11" : "November",
            "12" : "December"}

months_int = {"01":1,
            "02":2,
            "03":3,
            "04":4,
            "05":5,
            "06":6,
            "07":7,
            "08":8,
            "09": 9,
            "10" : 10,
            "11" : 11,
            "12" : 12}
#Connect to db
db = pymysql.connect(host='budgetwatcher.cfwqbytexmh5.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='vtece4574',
                             database='budgetWatcherDb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()#Db cursor
today = date.today()
# mm/dd/yy
d = today.strftime("%m/%d/%y")
date_string = d[0:2] + d[3:5] + "20" + d[6:8]
graph_expenses = True
graph_subscriptions = True

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("mainwindow.ui", self) #Retrieves ui from qt creator
        self.updateHomescreen()#Updates labels on home screen        
        chart = QChart()
        self.changeSeries(chart)     
        chartView = QChartView(chart)
        self.gridLayout_4.addWidget(chartView)   

        welcome = "Your expenses for " + months_map[date_string[0:2]] + ":"
        self.label_18.setText(welcome)

        #Edit budget button pressed
        self.pushButton.clicked.connect(self.on_pushButton)

        #Enter transactions button
        self.pushButton_2.clicked.connect(self.on_pushButton_2)

        #See transactions button
        self.pushButton_3.clicked.connect(self.on_pushButton_3)

        #See subscriptions pressed
        self.pushButton_11.clicked.connect(self.on_pushButton_11)

        #Back button on edit transactions
        self.pushButton_8.clicked.connect(lambda: self.on_pushButton_8(chart))

        #Back button on enter transactions
        self.pushButton_10.clicked.connect(lambda: self.on_pushButton_10(chart))

        #Back button on see transactions
        self.pushButton_12.clicked.connect(self.on_pushButton_12)

        #Back button on see subscriptions
        self.pushButton_13.clicked.connect(self.on_pushButton_13)

        #Done button on enter transactions-Housing
        self.pushButton_4.clicked.connect(self.on_pushButton_4)

        #Done button on enter transactions-Groceries
        self.pushButton_5.clicked.connect(self.on_pushButton_5)

        #Done button on enter transactions-Outtings
        self.pushButton_6.clicked.connect(self.on_pushButton_6)

        #Done button on add transaction
        self.pushButton_9.released.connect(self.on_pushButton_9)

        self.gridLayout_2.setRowStretch(0, 200)
        #Sets size of window
        self.setGeometry(100, 100, 1100, 600)
        self.show()

    def changeSeries(self, chart):
        #Adds up purchases in housing section from current month
        val = date_string[0:2] + "__" + date_string[4:8]
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        house_sum = result.get("SUM(purchase_amount)") 

        #Adds up purchases in grocery section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        groceries_sum = result.get("SUM(purchase_amount)")

        #Adds up purchases in outtings section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        outtings_sum = result.get("SUM(purchase_amount)")

        #Adds up purchases in the personal section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        personal_sum = result.get("SUM(purchase_amount)")

        #Gets proposed budget from db
        cursor.execute("SELECT * from user_budget")
        result = cursor.fetchone()        

        #Gets individual budget per category
        house_budget = result.get("House_Budget")
        groceries_budget = result.get("Groceries_Budget")
        outtings_budget = result.get("Outtings_Budget")
        personal_budget = result.get("Personal_Budget")

        budget_sum = house_budget + groceries_budget + outtings_budget + personal_budget
        # expense graph
        set0 = QBarSet('Housing')  # need to pull from db
        set1 = QBarSet('Groceries')
        set2 = QBarSet('Outings')
        set3 = QBarSet('Personal')
        set4 = QBarSet('Available funds')

        set0.append([house_sum])  # need to pull from db
        set1.append([groceries_sum])
        set2.append([outtings_sum])
        set3.append([personal_sum])
        set4.append([(budget_sum-set0[0]-set1[0]-set2[0]-set3[0])])

        series = QPercentBarSeries()  # !!!!!!!!!
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart.addSeries(series)
        chart.setTitle('Budget Usage')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        cur_month = months_map[date_string[0:2]]
        months = (cur_month)
        axisX = QBarCategoryAxis()
        axisX.append(months)
        axisY = QValueAxis()
        axisY.setRange(0, budget_sum)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

    
    #Sets up homescreen of labels from the budget
    def updateHomescreen(self):
        #Adds up purchases in housing section from current month
        val = date_string[0:2] + "__" + date_string[4:8]
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        house_sum = result.get("SUM(purchase_amount)") 

        #Adds up purchases in grocery section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        groceries_sum = result.get("SUM(purchase_amount)")

        #Adds up purchases in outtings section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        outtings_sum = result.get("SUM(purchase_amount)")

        #Adds up purchases in the personal section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        personal_sum = result.get("SUM(purchase_amount)")

        #Gets proposed budget from db
        cursor.execute("SELECT * from user_budget")
        result = cursor.fetchone()        

        #Gets individual budget per category
        house_budget = result.get("House_Budget")
        groceries_budget = result.get("Groceries_Budget")
        outtings_budget = result.get("Outtings_Budget")
        personal_budget = result.get("Personal_Budget")

        #Creates labels to be displayed on home screen
        house = '$' + str(round(house_sum, 2)) + ' / $' + str(round(house_budget, 2))
        groceries = '$' + str(round(groceries_sum, 2)) + ' / $' + str(round(groceries_budget, 2))
        outtings = '$' + str(round(outtings_sum, 2)) + ' / $' + str(round(outtings_budget, 2))
        personal = '$' + str(round(personal_sum, 2)) + ' / $' + str(round(personal_budget, 2))
        self.label_3.setText(house)
        if house_sum > house_budget:
            self.label_3.setStyleSheet("background-color: red;")
        elif house_sum > house_budget * .8:
            self.label_3.setStyleSheet("background-color: yellow;")

        self.label_4.setText(groceries)
        if groceries_sum > groceries_budget:
            self.label_4.setStyleSheet("background-color: red;")
        elif groceries_sum > groceries_budget * .8:
            self.label_4.setStyleSheet("background-color: yellow;")

        self.label_6.setText(outtings)
        if outtings_sum > outtings_budget:
            self.label_6.setStyleSheet("background-color: red;")
        elif outtings_sum > outtings_budget * .8:
            self.label_6.setStyleSheet("background-color: yellow;")

        self.label_8.setText(personal)
        if personal_sum > personal_budget:
            self.label_8.setStyleSheet("background-color: red;")
        elif personal_sum > personal_budget * .8:
            self.label_8.setStyleSheet("background-color: yellow;")
    #Sends us to edit budget screen
    def on_pushButton(self):
        self.stackedWidget.setCurrentIndex(1)

    #Sends us to enter transactions screen
    def on_pushButton_2(self):
        self.stackedWidget.setCurrentIndex(2)

    #See subscriptions button
    def on_pushButton_11(self):
        global graph_subscriptions
        self.stackedWidget.setCurrentIndex(4)
        set4 = QBarSet('Spotify')  # need to pull from db
        set5 = QBarSet('Netflix')
        set6 = QBarSet('Apple Music')

        valid = False
        # spotify
        try:
            cursor.execute("SELECT spotify FROM subscriptions WHERE sub_date = '082022';")
            spot_resultA = cursor.fetchone()
            spot_resultA = spot_resultA.get("spotify")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT spotify FROM subscriptions WHERE sub_date = '092022';")
            spot_resultS = cursor.fetchone()
            spot_resultS = spot_resultS.get("spotify")
            valid = True
        except:
            valid = False
        
        try:
            cursor.execute("SELECT spotify FROM subscriptions WHERE sub_date = '102022';")
            spot_resultO = cursor.fetchone()
            spot_resultO = spot_resultO.get("spotify")
            valid = True
        except:
            valid = False
        
        
        try:
            cursor.execute("SELECT spotify FROM subscriptions WHERE sub_date = '112022';")
            spot_resultN = cursor.fetchone()
            spot_resultN = spot_resultN.get("spotify")
            valid = True
        except:
            valid = False

        # Netflix
        try:
            cursor.execute("SELECT netflix FROM subscriptions WHERE sub_date = '082022';")
            net_resultA = cursor.fetchone()
            net_resultA = net_resultA.get("netflix")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT netflix FROM subscriptions WHERE sub_date = '092022';")
            net_resultS = cursor.fetchone()
            net_resultS = net_resultS.get("netflix")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT netflix FROM subscriptions WHERE sub_date = '102022';")
            net_resultO = cursor.fetchone()
            net_resultO = net_resultO.get("netflix")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT netflix FROM subscriptions WHERE sub_date = '112022';")
            net_resultN = cursor.fetchone()
            net_resultN = net_resultN.get("netflix")
            valid = True
        except:
            valid = False

        # Apple Music
        try:
            cursor.execute("SELECT apple_music FROM subscriptions WHERE sub_date = '082022';")
            appM_resultA = cursor.fetchone()
            appM_resultA = appM_resultA.get("apple_music")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT apple_music FROM subscriptions WHERE sub_date = '092022';")
            appM_resultS = cursor.fetchone()
            appM_resultS = appM_resultS.get("apple_music")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT apple_music FROM subscriptions WHERE sub_date = '102022';")
            appM_resultO = cursor.fetchone()
            appM_resultO = appM_resultO.get("apple_music")
            valid = True
        except:
            valid = False

        try:
            cursor.execute("SELECT apple_music FROM subscriptions WHERE sub_date = '112022';")
            appM_resultN = cursor.fetchone()
            appM_resultN = appM_resultN.get("apple_music")
            valid = True
        except:
            valid = False
        cursor.execute("SELECT * FROM subscriptions ;")
        set4.append([spot_resultA, spot_resultS, spot_resultO, spot_resultN])  # need to pull from db
        set5.append([net_resultA, net_resultS, net_resultO, net_resultN])
        set6.append([appM_resultA, appM_resultS, appM_resultO, appM_resultN])

        temp = [spot_resultA, spot_resultS, spot_resultO, spot_resultN, net_resultA, 
        net_resultS, net_resultO, net_resultN, appM_resultA, appM_resultS, appM_resultO, appM_resultN]
        ceiling = max(temp)

        series = QBarSeries()
        series.append(set4)
        series.append(set5)
        series.append(set6)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Subscription Usage')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Aug', 'Sept', 'Oct', 'Nov')
        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, ceiling)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        if graph_subscriptions:
            self.horizontalLayout_4.addWidget(chartView)
            graph_subscriptions = False
    
    #Sends us to see transactions screen
    def on_pushButton_3(self, chart):
        global graph_expenses
        self.stackedWidget.setCurrentIndex(3)
        set0 = QBarSet('Housing') 
        set1 = QBarSet('Groceries')
        set2 = QBarSet('Outings')
        set3 = QBarSet('Personal')

        #Adds up purchases in housing section from current month
        val = date_string[0:2] + "__" + date_string[4:8]

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        house_sum = result.get("SUM(purchase_amount)")


        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing' AND purchase_date LIKE (%s);", 
        "10__2022")
        result = cursor.fetchone()
        house_sum_2 = result.get("SUM(purchase_amount)") 

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing' AND purchase_date LIKE (%s);", 
        "09__2022")
        result = cursor.fetchone()
        house_sum_3 = result.get("SUM(purchase_amount)") 

        #Adds up purchases in grocery section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        groceries_sum = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries' AND purchase_date LIKE (%s);", 
        "10__2022")
        result = cursor.fetchone()
        groceries_sum_2 = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries' AND purchase_date LIKE (%s);", 
        "09__2022")
        result = cursor.fetchone()
        groceries_sum_3 = result.get("SUM(purchase_amount)")

        #Adds up purchases in outtings section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        outtings_sum = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings' AND purchase_date LIKE (%s);", 
        "10__2022")
        result = cursor.fetchone()
        outtings_sum_2 = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings' AND purchase_date LIKE (%s);", 
        "09__2022")
        result = cursor.fetchone()
        outtings_sum_3 = result.get("SUM(purchase_amount)")

        #Adds up purchases in the personal section from current month
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal' AND purchase_date LIKE (%s);", 
        val)
        result = cursor.fetchone()
        personal_sum = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal' AND purchase_date LIKE (%s);", 
        "10__2022")
        result = cursor.fetchone()
        personal_sum_2 = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal' AND purchase_date LIKE (%s);", 
        "09__2022")
        result = cursor.fetchone()
        personal_sum_3 = result.get("SUM(purchase_amount)")

        set0.append([house_sum_3, house_sum_2, house_sum])  
        set1.append([groceries_sum_3, groceries_sum_2, groceries_sum])
        set2.append([outtings_sum_3, outtings_sum_2, outtings_sum])
        set3.append([personal_sum_3, personal_sum_2, personal_sum])

        temp = [house_sum_3, house_sum_2, house_sum, groceries_sum_3, groceries_sum_2, groceries_sum,
        outtings_sum_3, outtings_sum_2, outtings_sum, personal_sum_3, personal_sum_2, personal_sum]
        ceiling = max(temp)
        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Past Spending')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Sept', 'Oct', 'Nov')
        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, ceiling)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        if graph_expenses:
            self.horizontalLayout_3.addWidget(chartView)
            graph_expenses = False

    #Back button - edit budget screen
    def on_pushButton_8(self, chart):
        self.stackedWidget.setCurrentIndex(0)
        self.updateHomescreen()
    
    #Back button - enter transactions screen
    def on_pushButton_10(self, chart):
        self.stackedWidget.setCurrentIndex(0)
        self.updateHomescreen()

    #Back button - see transactions screen
    def on_pushButton_12(self):
        self.stackedWidget.setCurrentIndex(0)

    #Back button - see subscriptions screen
    def on_pushButton_13(self):
        self.stackedWidget.setCurrentIndex(0)
    
    #Updates database to edit home budget
    def on_pushButton_4(self):
        new_budget = self.lineEdit.text()
        cursor.execute("UPDATE user_budget SET House_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.lineEdit.clear()
        self.updateHomescreen()
    #Updates database to edit groceries budget
    def on_pushButton_5(self):
        new_budget = self.lineEdit_2.text()
        cursor.execute("UPDATE user_budget SET Groceries_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.lineEdit_2.clear()
        self.updateHomescreen()
    #Updates database to edit outtings budget
    def on_pushButton_6(self):
        new_budget = self.lineEdit_3.text()
        cursor.execute("UPDATE user_budget SET Outtings_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.lineEdit_3.clear()
        self.updateHomescreen()
    #Updates database to edit personal budget
    def on_pushButton_7(self):
        new_budget = self.lineEdit_4.text()
        cursor.execute("UPDATE user_budget SET Personal_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.lineEdit_4.clear()
        self.updateHomescreen()

    #creates new purchase
    def on_pushButton_9(self):
        comboBox_map= {0: "Housing",
                        1: "Outtings",
                        2: "Personal",
                        3: "Groceries"}
        purchase_id = random.randint(1000, 9999)
        date = self.lineEdit_5.text()
        name = self.lineEdit_6.text()
        amount = self.lineEdit_7.text()
        p_type = comboBox_map[self.comboBox.currentIndex()]
        val = (purchase_id, 1, p_type, date, name, amount)
        cursor.execute("INSERT INTO customer_purchases (purchase_id, customer_id, purchase_type, purchase_date, purchase_name, purchase_amount) VALUES ((%s), (%s), (%s), (%s), (%s), (%s));", 
        val)
        db.commit()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.updateHomescreen()

def main ():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()