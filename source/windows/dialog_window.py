from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QSize
from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow

from modules.settings import *
from ui.dialog_window_design import Ui_DialogWindow
from windows.base_window import BaseWindow


class DialogWindow(QMainWindow, BaseWindow, Ui_DialogWindow):
    def __init__(self, parent, text="Dialog Window", text1="OK", text2=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

        self.setWindowTitle("Warning")
        self.InfoLabel.setText(text)
        self.IconButton.setProperty("Icon", True)

        if self.AcceptButton.sizeHint().width() > self.CancelButton.sizeHint().width():
            width = self.AcceptButton.sizeHint().width()
        else:
            width = self.AcceptButton.sizeHint().width()

        self.AcceptButton.setFixedWidth(width + 16)
        self.CancelButton.setFixedWidth(width + 16)

        if text2 is None:
            self.CancelButton.hide()

        self.AcceptButton.setText(text1)

        self.AcceptButton.clicked.connect(self.close)
        self.CancelButton.clicked.connect(self.close)

        self.show()
