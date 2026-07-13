#pragma once
#include <QObject>

class Button : public QObject {
    Q_OBJECT
public:
    explicit Button(QObject* parent = nullptr) : QObject(parent) {}
signals:
    void clicked(int x);
public:
    void press(int x) { emit clicked(x); }
};

class Label : public QObject {
    Q_OBJECT
public slots:
    void on_clicked(int x);
};
