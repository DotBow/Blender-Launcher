import resources_rc
from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 768))
        self.CentralWidget = QtWidgets.QWidget(MainWindow)
        self.CentralWidget.setObjectName("CentralWidget")
        self.CentralLayout = QtWidgets.QVBoxLayout(self.CentralWidget)
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        self.CentralLayout.setObjectName("CentralLayout")
        MainWindow.setCentralWidget(self.CentralWidget)
        self.MenuBar = QtWidgets.QMenuBar(MainWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.MenuBar.setObjectName("MenuBar")
        MainWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QtWidgets.QStatusBar(MainWindow)
        self.StatusBar.setObjectName("StatusBar")
        MainWindow.setStatusBar(self.StatusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
