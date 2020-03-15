from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QMainWindow


class BaseWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pos = self.pos()
        self.pressing = False

    def mousePressEvent(self, event):
        self.pos = event.globalPos()
        self.pressing = True
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.pressing:
            delta = QPoint(event.globalPos() - self.pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.pos = event.globalPos()

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
        self.setCursor(Qt.ArrowCursor)
