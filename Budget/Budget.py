from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from datetime import date
from PyQt5 import uic
from PyQt5.Qt import Qt
import random
import pymysql

months_map = {"01":"January",
            "09": "September",
            "10" : "October",
            "11" : "November",
            "12" : "December"}
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
date_string = d[0:2] + d[3:5] + "20" +d[6:8]


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

        #Back button on edit transactions
        self.pushButton_8.clicked.connect(self.on_pushButton_8)

        #Back button on enter transactions
        self.pushButton_10.clicked.connect(self.on_pushButton_10)

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
        # house_sum = 2000
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
        # house_sum = 2000
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
        house = '$' + str(house_sum) + ' / $' + str(house_budget)
        groceries = '$' + str(groceries_sum) + ' / $' + str(groceries_budget)
        outtings = '$' + str(outtings_sum) + ' / $' + str(outtings_budget)
        personal = '$' + str(personal_sum) + ' / $' + str(personal_budget)
        self.label_3.setText(house)
        self.label_4.setText(groceries)
        self.label_6.setText(outtings)
        self.label_8.setText(personal)

    #Sends us to edit budget screen
    def on_pushButton(self):
        self.stackedWidget.setCurrentIndex(1)

    #Sends us to enter transactions screen
    def on_pushButton_2(self):
        self.stackedWidget.setCurrentIndex(2)

    #Sends us to see transactions screen
    def on_pushButton_3(self):
        self.stackedWidget.setCurrentIndex(3)

    #Back button - edit transactions screen
    def on_pushButton_8(self):
        self.stackedWidget.setCurrentIndex(0)
    
    #Back button - enter transactions screen
    def on_pushButton_10(self):
        self.stackedWidget.setCurrentIndex(0)
    
    #Updates database to edit home budget
    def on_pushButton_4(self):
        new_budget = self.lineEdit.text()
        cursor.execute("UPDATE user_budget SET House_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()
    #Updates database to edit groceries budget
    def on_pushButton_5(self):
        new_budget = self.lineEdit_2.text()
        cursor.execute("UPDATE user_budget SET Groceries_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()
    #Updates database to edit outtings budget
    def on_pushButton_6(self):
        new_budget = self.lineEdit_3.text()
        cursor.execute("UPDATE user_budget SET Outtings_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()
    #Updates database to edit personal budget
    def on_pushButton_7(self):
        new_budget = self.lineEdit_4.text()
        cursor.execute("UPDATE user_budget SET Personal_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
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
        print(p_type)
        val = (purchase_id, 1, p_type, date, name, amount)
        cursor.execute("INSERT INTO customer_purchases (purchase_id, customer_id, purchase_type, purchase_date, purchase_name, purchase_amount) VALUES ((%s), (%s), (%s), (%s), (%s), (%s));", 
        val)
        db.commit()
        self.updateHomescreen()

def main ():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()