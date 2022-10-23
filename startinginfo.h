#ifndef STARTINGINFO_H
#define STARTINGINFO_H

#include <QDialog>

namespace Ui {
class StartingInfo;
}

class StartingInfo : public QDialog
{
    Q_OBJECT

public:
    explicit StartingInfo(QWidget *parent = nullptr);
    ~StartingInfo();

private slots:

private:
    Ui::StartingInfo *ui;
};

#endif // STARTINGINFO_H
