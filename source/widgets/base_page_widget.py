from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

from widgets.base_list_widget import BaseListWidget


class BasePageWidget(QWidget):
    def __init__(self, parent, text):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Placeholder Widget
        self.PlaceholderWidget = QWidget()
        self.PlaceholderWidget.setProperty("ToolBoxWidget", True)
        self.PlaceholderLayout = QHBoxLayout(self.PlaceholderWidget)
        self.PlaceholderLayout.setContentsMargins(0, 0, 0, 0)

        self.InfoPixmap = QPixmap(":resources/icons/info.svg")
        self.InfoPixmapLabel = QLabel()
        self.InfoPixmapLabel.setScaledContents(True)
        self.InfoPixmapLabel.setFixedSize(32, 32)
        self.InfoPixmapLabel.setPixmap(self.InfoPixmap)

        self.InfoLabelLayout = QHBoxLayout()
        self.InfoLabelLayout.setContentsMargins(0, 0, 0, 6)
        self.InfoLabel = QLabel(text)
        self.InfoLabelLayout.addWidget(self.InfoLabel)

        self.list_widget = BaseListWidget(self)
        self.list_widget.hide()

        self.PlaceholderLayout.addStretch()
        self.PlaceholderLayout.addWidget(self.InfoPixmapLabel)
        self.PlaceholderLayout.addLayout(self.InfoLabelLayout)
        self.PlaceholderLayout.addStretch()

        # Header Widget
        self.HeaderWidget = QWidget()
        self.HeaderWidget.hide()
        self.HeaderWidget.setProperty("ToolBoxWidget", True)
        self.HeaderLayout = QHBoxLayout(self.HeaderWidget)
        self.HeaderLayout.setContentsMargins(2, 2, 2, 2)

        self.fakeLabel = QLabel()
        self.subversionLabel = QLabel("Version")
        self.subversionLabel.setAlignment(Qt.AlignCenter)
        self.branchLabel = QLabel("Branch")
        self.branchLabel.setAlignment(Qt.AlignCenter)
        self.commitTimeLabel = QLabel("Commit Time")
        self.commitTimeLabel.setAlignment(Qt.AlignCenter)
        self.buildHashLabel = QLabel("Hash")
        self.buildHashLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.fakeLabel)
        self.HeaderLayout.addWidget(self.subversionLabel)
        self.HeaderLayout.addWidget(self.branchLabel)
        self.HeaderLayout.addWidget(self.commitTimeLabel)
        self.HeaderLayout.addWidget(self.buildHashLabel)
        self.HeaderLayout.addStretch()

        # Final layout
        self.layout.addWidget(self.HeaderWidget)
        self.layout.addWidget(self.PlaceholderWidget)
        self.layout.addWidget(self.list_widget)

    def set_info_label_text(self, text):
        self.InfoLabel.setText(text)
