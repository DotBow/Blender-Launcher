from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu


class BaseMenuWidget(QMenu):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.NoDropShadowWindowHint)
