from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu


class BaseMenuWidget(QMenu):
    height = 30

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.NoDropShadowWindowHint)
        self.height = BaseMenuWidget.height

    def _show(self, reverse=False):
        cursor = QCursor.pos()
        cursor.setX(cursor.x() - self.height * 0.5)
        actions = self.actions()

        if reverse:
            actions.reverse()
            actions_count = sum((a.isVisible() and not a.isSeparator())
                                for a in actions)
            cursor.setY(cursor.y() - actions_count * self.height + 15)
        else:
            cursor.setY(cursor.y() - self.height * 0.5)

        i = 0

        for action in actions:
            if action.isVisible() and not action.isSeparator():
                if action.isEnabled():
                    self.setActiveAction(action)
                    cursor.setY(cursor.y() + i *
                                (self.height if reverse else (- self.height)))
                    break

                i = i + 1

        self.exec_(cursor)
