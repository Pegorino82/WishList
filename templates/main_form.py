# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.11
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.browser = QtWidgets.QTableWidget(self.centralwidget)
        self.browser.setObjectName("browser")
        self.browser.setColumnCount(5)
        self.browser.setRowCount(0)

        header = self.browser.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        item = QtWidgets.QTableWidgetItem()
        self.browser.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.browser.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.browser.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.browser.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.browser.setHorizontalHeaderItem(4, item)

        self.browser.hideColumn(0)

        self.verticalLayout.addWidget(self.browser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setObjectName("createButton")
        self.horizontalLayout.addWidget(self.createButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.browser.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.browser.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Название"))
        item = self.browser.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Цена"))
        item = self.browser.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Ссылка"))
        item = self.browser.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Описание"))
        self.createButton.setText(_translate("MainWindow", "Добавить"))

