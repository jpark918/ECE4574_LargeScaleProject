from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic
import pymysql


db = pymysql.connect(host='budgetwatcher.cfwqbytexmh5.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='vtece4574',
                             database='budgetWatcherDb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
print(db)
cursor = db.cursor()

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.gridLayout.setRowStretch(4,2)
        self.gridLayout.setColumnMinimumWidth(1, 80000)

        cursor.execute("SELECT * from customers")
        result = cursor.fetchall()
        print(result)
        info = "Did it work?"
        self.label_3.setText(info)
        self.setGeometry(100, 100, 800, 300)
        self.show()

def main ():
    app = QApplication([])
    # window = QWidget()
    # window.setGeometry(100, 100, 700, 700)
    # window.setWindowTitle("My Simple GUI")

    # layout = QVBoxLayout()

    # label = QLabel("Press the Button Below")
    # button = QPushButton("Press Me!")

    # layout.addWidget(label)
    # layout.addWidget(button)

    # window.setLayout(layout)

    # button.clicked.connect(on_clicked)
    # window.show()
    window = MyGUI()
    app.exec_()

def on_clicked():
    message = QMessageBox()
    message.setText("Hello World")
    message.exec_()
if __name__ == '__main__':
    main()