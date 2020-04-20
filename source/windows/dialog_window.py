from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from modules.settings import *
from ui.dialog_window_design import Ui_DialogWindow
from windows.base_window import BaseWindow


class DialogWindow(QMainWindow, BaseWindow, Ui_DialogWindow):
    accepted = pyqtSignal()
    cancelled = pyqtSignal()

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

        self.AcceptButton.clicked.connect(self.accept)
        self.CancelButton.clicked.connect(self.cancel)

        self.show()

    def accept(self):
        self.accepted.emit()
        self.close()

    def cancel(self):
        self.cancelled.emit()
        self.close()
