from PyQt5.QtWidgets import *
from PyQt5 import uic
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
        uic.loadUi("mainwindow.ui", self)

        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Housing';")
        result = cursor.fetchone()
        house_sum = result.get("SUM(purchase_amount)") 
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Groceries';")
        result = cursor.fetchone()
        groceries_sum = result.get("SUM(purchase_amount)")
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Outtings';")
        result = cursor.fetchone()
        outtings_sum = result.get("SUM(purchase_amount)")
        cursor.execute("SELECT SUM(purchase_amount) FROM customer_purchases WHERE purchase_type = 'Personal';")
        result = cursor.fetchone()
        personal_sum = result.get("SUM(purchase_amount)")

        cursor.execute("SELECT * from user_budget")
        result = cursor.fetchone()        

        house_budget = result.get("House_Budget")
        groceries_budget = result.get("Groceries_Budget")
        outtings_budget = result.get("Outtings_Budget")
        personal_budget = result.get("Personal_Budget")

        house = '$' + str(house_sum) + ' / $' + str(house_budget)
        groceries = '$' + str(groceries_sum) + ' / $' + str(groceries_budget)
        outtings = '$' + str(outtings_sum) + ' / $' + str(outtings_budget)
        personal = '$' + str(personal_sum) + ' / $' + str(personal_budget)
        self.label_3.setText(house)
        self.label_4.setText(groceries)
        self.label_6.setText(outtings)
        self.label_8.setText(personal)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)
        self.pushButton_8.clicked.connect(self.on_pushButton_8_clicked)
        self.pushButton_10.clicked.connect(self.on_pushButton_10_clicked)
        self.setGeometry(100, 100, 800, 300)
        self.show()
    def on_pushButton_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
    def on_pushButton_2_clicked(self):
        self.stackedWidget.setCurrentIndex(2)
    def on_pushButton_3_clicked(self):
        self.stackedWidget.setCurrentIndex(3)
    def on_pushButton_8_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
    def on_pushButton_10_clicked(self):
        self.stackedWidget.setCurrentIndex(0)


def main ():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()