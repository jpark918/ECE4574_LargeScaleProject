import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic
import pymysql
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter

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
        # Load the ui file
        uic.loadUi("mainwindow.ui", self)
        self.gridLayout.setRowStretch(4,2)
        self.gridLayout.setColumnMinimumWidth(1, 80000)

        cursor.execute("SELECT * from customers")
        result = cursor.fetchall()
        print(result)
        info = "Did it work?"
        self.label_3.setText(info)
        self.setGeometry(100, 100, 800, 300)

        #Define Our Widgets
        self.button3 = self.findChild(QPushButton, "pushButton_3")

        #Do something
        self.button3.clicked.connect(self.on_clicked)

        #show the app
        self.show()

    def on_clicked(self):
        set0 = QBarSet('Netflix')  # need to pull from db
        set1 = QBarSet('Spotify')
        set2 = QBarSet('Apple Music')

        set0.append([2, 6, 21, 10])  # need to pull from db
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
        # months = ('gruyere', 'colby', 'pepper jack', 'american')
        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, 50)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        self.setCentralWidget(chartView)
        #message = QMessageBox()
        #message.setText("Hello World")
        #message.exec_()


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

if __name__ == '__main__':
    main()