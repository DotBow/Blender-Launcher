# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SettingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.SettingsButton.setObjectName("SettingsButton")
        self.horizontalLayout.addWidget(self.SettingsButton, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.LibraryTab = QtWidgets.QWidget()
        self.LibraryTab.setObjectName("LibraryTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.LibraryTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LibraryListWidget = QtWidgets.QListWidget(self.LibraryTab)
        self.LibraryListWidget.setObjectName("LibraryListWidget")
        self.verticalLayout.addWidget(self.LibraryListWidget)
        self.tabWidget.addTab(self.LibraryTab, "")
        self.DownloadsTab = QtWidgets.QWidget()
        self.DownloadsTab.setObjectName("DownloadsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.DownloadsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.DownloadsListWidget = QtWidgets.QListWidget(self.DownloadsTab)
        self.DownloadsListWidget.setObjectName("DownloadsListWidget")
        self.verticalLayout_3.addWidget(self.DownloadsListWidget)
        self.tabWidget.addTab(self.DownloadsTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SettingsButton.setText(_translate("MainWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LibraryTab), _translate("MainWindow", "Library"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DownloadsTab), _translate("MainWindow", "Downloads"))

import resources.resources_rc
