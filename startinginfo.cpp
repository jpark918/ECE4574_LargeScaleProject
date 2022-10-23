#include "startinginfo.h"
#include "ui_startinginfo.h"

StartingInfo::StartingInfo(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::StartingInfo)
{
    ui->setupUi(this);
}

StartingInfo::~StartingInfo()
{
    delete ui;
}
