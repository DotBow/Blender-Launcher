from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDesktopWidget, QMenu


class BaseMenuWidget(QMenu):
    action_height = 30

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.NoDropShadowWindowHint)
        self.action_height = BaseMenuWidget.action_height
        self.screen_size = QDesktopWidget().screenGeometry()

    def _show(self):
        actions = self.actions()
        actions_count = sum((a.isVisible() and not a.isSeparator())
                            for a in actions)

        if actions_count == 0:
            return

        menu_height = actions_count * self.action_height
        reverse = False

        cursor = QCursor.pos()
        cursor.setX(cursor.x() - self.action_height * 0.5)

        if cursor.y() > (self.screen_size.height() - menu_height):
            reverse = True

        if reverse:
            actions.reverse()
            cursor.setY(cursor.y() - actions_count * self.action_height + 15)
        else:
            cursor.setY(cursor.y() - self.action_height * 0.5)

        i = 0

        for action in actions:
            if action.isVisible() and not action.isSeparator():
                if action.isEnabled():
                    self.setActiveAction(action)
                    cursor.setY(cursor.y() + i *
                                (self.action_height if reverse
                                 else (- self.action_height)))
                    break

                i = i + 1

        self.exec_(cursor)
