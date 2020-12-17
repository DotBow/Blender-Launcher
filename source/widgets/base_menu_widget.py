from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu


class BaseMenuWidget(QMenu):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.NoDropShadowWindowHint)

    def _show(self):
        cursor = QCursor.pos()
        cursor = cursor - QPoint(15, 15)
        i = 0

        for action in self.actions():
            if action.isVisible() and action.isEnabled():
                self.setActiveAction(action)
                cursor.setY(cursor.y() - i * 30)
                break

            i = i + 1

        self.exec_(cursor)
