#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include "startinginfo.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QLineSeries *series = new QLineSeries();
    series->append(0,6);
    series->append(2,4);
    series->append(3,8);
    series->append(7,4);
    series->append(10,5);

    *series << QPointF(11,1) << QPointF(13,3) << QPointF(17,6) << QPointF(18,3)
            << QPointF(20,2);

    QChart *chart = new QChart();
    //chart->legend()->hide();
    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);
    //chart->legend()->setAlignment(Qt::Align)
    chart->addSeries(series);
    chart->createDefaultAxes();
    chart->setTitle("Website average visits");

    //allowing the chart to be seen on runtime
    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setParent(ui->horizontalFrame);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_lineEdit_returnPressed()
{
    StartingInfo budget;
    budget.setModal(true); //model approach, the second window must be closed in order to access the first
    budget.exec();
}

