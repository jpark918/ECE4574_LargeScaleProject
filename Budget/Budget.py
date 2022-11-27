from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5 import uic
from PyQt5.Qt import Qt
import pymysql

#Connect to db
db = pymysql.connect(host='budgetwatcher.cfwqbytexmh5.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='vtece4574',
                             database='budgetWatcherDb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()#Db cursor

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("mainwindow.ui", self) #Retrieves ui from qt creator
        self.updateHomescreen()

        #Edit budget button pressed
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

        #Enter transactions button
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)

        #See transactions button
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)

        #Back button on edit transactions
        self.pushButton_8.clicked.connect(self.on_pushButton_8_clicked)

        #Back button on enter transactions
        self.pushButton_10.clicked.connect(self.on_pushButton_10_clicked)

        #Done button on enter transactions-Housing
        self.pushButton_4.clicked.connect(self.on_pushButton_4_clicked)

        #Done button on enter transactions-Groceries
        self.pushButton_5.clicked.connect(self.on_pushButton_5_clicked)

        #Done button on enter transactions-Outtings
        self.pushButton_6.clicked.connect(self.on_pushButton_6_clicked)

        #Sets size of window
        self.setGeometry(100, 100, 800, 300)
        self.show()
    
    #Sets up homescreen of labels from the budget
    def updateHomescreen(self):
        #Adds up purchases in housing section
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing';")
        result = cursor.fetchone()
        house_sum = result.get("SUM(purchase_amount)") 

        #Adds up purchases in grocery section
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries';")
        result = cursor.fetchone()
        groceries_sum = result.get("SUM(purchase_amount)")

        #Adds up purchases in outtings section
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings';")
        result = cursor.fetchone()
        outtings_sum = result.get("SUM(purchase_amount)")

        #Adds up purchases in the personal section
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal';")
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

        set0 = QBarSet('Netflix')
        set1 = QBarSet('Spotify')
        set2 = QBarSet('Apple Music')

        set0.append([2, 6, 21, 10])
        set1.append([20, 15, 18, 9])
        set2.append([15, 18, 7, 21])

        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Web Subscriptions')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Sept', 'Oct', 'Nov', 'Dec')
        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, 50)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        self.gridLayout_4.addWidget(chartView)
        # self.setCentralWidget(chartView)

    #Sends us to edit budget screen
    def on_pushButton_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    #Sends us to enter transactions screen
    def on_pushButton_2_clicked(self):
        self.stackedWidget.setCurrentIndex(2)

    #Sends us to see transactions screen
    def on_pushButton_3_clicked(self):
        self.stackedWidget.setCurrentIndex(3)

    #Back button - edit transactions screen
    def on_pushButton_8_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
    
    #Back button - enter transactions screen
    def on_pushButton_10_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
    
    #Updates database to edit home budget
    def on_pushButton_4_clicked(self):
        new_budget = self.lineEdit.text()
        cursor.execute("UPDATE user_budget SET House_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()
    #Updates database to edit groceries budget
    def on_pushButton_5_clicked(self):
        new_budget = self.lineEdit_2.text()
        cursor.execute("UPDATE user_budget SET Groceries_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()
    #Updates database to edit outtings budget
    def on_pushButton_6_clicked(self):
        new_budget = self.lineEdit_3.text()
        cursor.execute("UPDATE user_budget SET Outtings_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()
    #Updates database to edit personal budget
    def on_pushButton_7_clicked(self):
        new_budget = self.lineEdit_4.text()
        cursor.execute("UPDATE user_budget SET Personal_Budget = (%s) WHERE Customer_ID = 1;", new_budget)
        db.commit()
        self.updateHomescreen()

def main ():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()