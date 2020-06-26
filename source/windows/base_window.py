from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget

from modules.settings import *

if get_enable_high_dpi_scaling():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class BaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.parent = parent
        self.pos = self.pos()
        self.pressing = False

    def mousePressEvent(self, event):
        self.pos = event.globalPos()
        self.pressing = True
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.pressing:
            delta = QPoint(event.globalPos() - self.pos)
            self.moveWindow(delta)
            self.pos = event.globalPos()

    def moveWindow(self, delta):
        self.move(self.x() + delta.x(), self.y() + delta.y())

        if self.parent is not None:
            self.parent.moveWindow(delta)

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
        self.setCursor(Qt.ArrowCursor)

    def showEvent(self, event):
        if self.parent is not None:
            if self.parent.isVisible():
                x = self.parent.x() + (self.parent.width() - self.width()) * 0.5
                y = self.parent.y() + (self.parent.height() - self.height()) * 0.5
            else:
                size = self.parent.app.screens()[0].size()
                x = (size.width() - self.width()) * 0.5
                y = (size.height() - self.height()) * 0.5

            self.move(x, y)
            event.accept()
