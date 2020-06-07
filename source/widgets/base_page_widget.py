from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from widgets.base_list_widget import BaseListWidget


class BasePageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setProperty("ToolBoxWidget", True)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.PlaceholderWidget = QWidget()
        self.PlaceholderWidget.setProperty("ToolBoxWidget", True)
        self.PlaceholderWidget.setObjectName("PlaceholderWidget")
        self.PlaceholderLayout = QHBoxLayout(self.PlaceholderWidget)
        self.PlaceholderLayout.setContentsMargins(0, 0, 0, 0)
        self.InfoPximap = QPixmap(":resources/icons/info.svg")
        self.InfoPximapLabel = QLabel()
        self.InfoPximapLabel.setScaledContents(True)
        self.InfoPximapLabel.setFixedSize(32, 32)
        self.InfoPximapLabel.setPixmap(self.InfoPximap)
        self.PlaceholderLayout.addStretch()
        self.PlaceholderLayout.addWidget(self.InfoPximapLabel)
        self.PlaceholderLayout.addWidget(QLabel("Nothing to show yet"))
        self.PlaceholderLayout.addStretch()
        self.layout.addWidget(self.PlaceholderWidget)

        self.list_widget = BaseListWidget(self)
        self.layout.addWidget(self.list_widget)
        self.list_widget.hide()
