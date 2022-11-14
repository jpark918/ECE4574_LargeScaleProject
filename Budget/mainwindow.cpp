#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QSqlDatabase>
#include <QMessageBox>
#include <QSql>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_clicked()
{
    ui->stackedWidget->setCurrentIndex(1);
}


void MainWindow::on_pushButton_2_clicked()
{
    ui->stackedWidget->setCurrentIndex(2);
}


void MainWindow::on_pushButton_3_clicked()
{
    ui->stackedWidget->setCurrentIndex(3);
}


void MainWindow::on_pushButton_4_clicked()
{

}


void MainWindow::on_pushButton_8_clicked()
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL");
    db.setHostName("127.0.0.1");
    db.setDatabaseName("budgetWatcherDb");
    db.setUserName("admin");
    db.setPassword("vtece4574");

    if (db.open())
    {
        QMessageBox ::information(this, "Connection", "Database connected");
    }
    else
    {
        QMessageBox ::information(this, "Not Connected", "Database not connected");
    }
}

