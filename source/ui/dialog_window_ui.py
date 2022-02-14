from PyQt5 import QtCore, QtWidgets


class Ui_DialogWindow(object):
    def setupUi(self, DialogWindow):
        DialogWindow.setObjectName("DialogWindow")
        DialogWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogWindow.resize(160, 60)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            DialogWindow.sizePolicy().hasHeightForWidth())
        DialogWindow.setSizePolicy(sizePolicy)
        self.CentralWidget = QtWidgets.QWidget(DialogWindow)
        self.CentralWidget.setObjectName("CentralWidget")
        self.CentralLayout = QtWidgets.QVBoxLayout(self.CentralWidget)
        self.CentralLayout.setContentsMargins(6, 6, 6, 6)
        self.CentralLayout.setSpacing(0)
        self.CentralLayout.setObjectName("CentralLayout")
        DialogWindow.setCentralWidget(self.CentralWidget)
