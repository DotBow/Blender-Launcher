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

        self.InfoPixmap = QPixmap(":resources/icons/info.svg")
        self.InfoPixmapLabel = QLabel()
        self.InfoPixmapLabel.setScaledContents(True)
        self.InfoPixmapLabel.setFixedSize(32, 32)
        self.InfoPixmapLabel.setPixmap(self.InfoPixmap)

        self.InfoLabelLayout = QHBoxLayout()
        self.InfoLabelLayout.setContentsMargins(0, 0, 0, 6)
        self.InfoLabelLayout.addWidget(QLabel("Nothing to show yet"))

        self.list_widget = BaseListWidget(self)
        self.list_widget.hide()

        self.PlaceholderLayout.addStretch()
        self.PlaceholderLayout.addWidget(self.InfoPixmapLabel)
        self.PlaceholderLayout.addLayout(self.InfoLabelLayout)
        self.PlaceholderLayout.addStretch()

        self.layout.addWidget(self.PlaceholderWidget)
        self.layout.addWidget(self.list_widget)
