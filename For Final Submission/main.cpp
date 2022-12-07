#include "mainwindow.h"

#include <QApplication>

#include <QtWidgets/QMainWindow>
#include <QtCharts/QChartView>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QLegend>
#include <QtCharts/QBarCategoryAxis>
#include <QtCharts/QHorizontalStackedBarSeries>
#include <QtCharts/QLineSeries>
#include <QtCharts/QCategoryAxis>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>

QT_CHARTS_USE_NAMESPACE
#include <iostream>
#include <QString>
#include <QDebug>
using namespace std;

 /*
  *	main.cpp Park 
  *	
  * (OUTDATED)
  *	This is the original c++ implementation 
  *	to create graphs in qt creator.
  *	The initial design asks for the user to type in their data
  * before it gets used as a data set.
  */



QString getInput(){
    const int BUFSIZE = 1024;
    char buffer[BUFSIZE];

    std::cin.getline(buffer,BUFSIZE);
    return QString(buffer);
}

int main(int argc, char *argv[])
{

    //QString input = getInput();
    std::string input;
    // qPrintable() because cout can't handle QStrings

    //std::cout << "Enter budget (for month): " << qPrintable(input) << std::endl;
    std::cout << "Enter budget (for month): " << input << std::endl;
    //std::cout << "Enter budget (for month): " << std::endl;
    qDebug() << "Hello";

   QApplication a(argc, argv);
   MainWindow w;
    w.show();
   // return a.exec();

   QBarSet *set0 = new QBarSet("Netflix");
   QBarSet *set1 = new QBarSet("Hulu");
   QBarSet *set2 = new QBarSet("Disney+");
   QBarSet *set3 = new QBarSet("HBO");

   //dup
   QBarSet *set4 = new QBarSet("Housing");
   QBarSet *set5 = new QBarSet("Groceries");
   QBarSet *set6 = new QBarSet("Outings");
   QBarSet *set7 = new QBarSet("Personal Expenses");

   *set0 << 283 << 341 << 313 << 338 << 346 << 335;
   *set1 << 250 << 315 << 282 << 307 << 303 << 330;
   *set2 << 294 << 246 << 257 << 319 << 300 << 325;
   *set3 << 248 << 244 << 265 << 281 << 278 << 313;

   //previous
   *set4 << 2000 << 570 << 150 << 120;
   *set5 << 1000 << 303 << 300 << 90;
   *set6 << 900 << 230 << 600 << 60;
   *set7 << 200 << 120 << 900 << 20;

   QBarSeries *series = new QBarSeries();  

   //dup spent
   QBarSeries *series2 = new QBarSeries();

   series->append(set0);
   series->append(set1);
   series->append(set2);
   series->append(set3);

   //dup
   series2->append(set4);
   series2->append(set5);
   series2->append(set6);
   series2->append(set7);

   QChart *chart = new QChart();
   chart->addSeries(series);
   chart->setTitle("Avg visits by Month");
   //noAnimation, GridAxisAnimations, SeriesAnimations
   chart->setAnimationOptions(QChart::AllAnimations);
   QStringList categories;
   categories << "Jan" << "Feb" << "Mar" << "Apr";
   QBarCategoryAxis *axis = new QBarCategoryAxis();
   axis->append(categories);
   chart->createDefaultAxes();
   chart->setAxisX(axis, series);
   chart->legend()->setVisible(true);
   chart->legend()->setAlignment(Qt::AlignBottom);

   QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    QPalette pal = qApp->palette();
    pal.setColor(QPalette::Window, QRgb(0xffffff));
    pal.setColor(QPalette::WindowText, QRgb(0x404040));
    qApp->setPalette(pal);

   QMainWindow window;
   window.setCentralWidget(chartView);
   window.show();

   //dup
   QChart *chart2 = new QChart();
   chart2->addSeries(series2);
   chart2->setTitle("Monthly expenditures");
   chart2->setAnimationOptions(QChart::AllAnimations);
   QStringList categories2;
   categories2 << "Jan" << "Feb" << "Mar" << "Apr";
   QBarCategoryAxis *axis2 = new QBarCategoryAxis();
   axis2->append(categories2);
   chart2->createDefaultAxes();
   chart2->setAxisX(axis2, series2);
   chart2->legend()->setVisible(true);
   chart2->legend()->setAlignment(Qt::AlignBottom);

   QChartView *chartView2 = new QChartView(chart2);
   chartView2->setRenderHint(QPainter::Antialiasing);
   QPalette pal2 = qApp->palette();
   pal2.setColor(QPalette::Window, QRgb(0xffffff));
   pal2.setColor(QPalette::WindowText, QRgb(0x404040));
   qApp->setPalette(pal2);
   QMainWindow window2;
   window2.setCentralWidget(chartView2);
   window2.show();
    //end dup

   return a.exec();
}
