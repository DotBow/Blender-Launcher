from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget)

from modules.settings import get_list_sorting_type, set_list_sorting_type
from widgets.base_list_widget import BaseListWidget


class SortingType(Enum):
    DATETIME = 1
    VERSION = 2


class BasePageWidget(QWidget):
    def __init__(self, parent, text, name, show_hash=True):
        super().__init__()
        self.name = name

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
        self.HeaderLayout.setContentsMargins(2, 0, 2, 0)

        self.fakeLabel = QLabel()
        self.subversionLabel = QPushButton("Version")
        self.subversionLabel.setProperty("ListHeader", True)
        self.subversionLabel.setCheckable(True)
        self.subversionLabel.clicked.connect(
            lambda: self.set_sorting_type(SortingType.VERSION))
        self.branchLabel = QLabel("Branch")
        self.branchLabel.setAlignment(Qt.AlignCenter)
        self.commitTimeLabel = QPushButton("Commit Time")
        self.commitTimeLabel.setProperty("ListHeader", True)
        self.commitTimeLabel.setCheckable(True)
        self.commitTimeLabel.clicked.connect(
            lambda: self.set_sorting_type(SortingType.DATETIME))
        self.buildHashLabel = QLabel("Hash")
        self.buildHashLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.fakeLabel)
        self.HeaderLayout.addWidget(self.subversionLabel)
        self.HeaderLayout.addWidget(self.branchLabel)
        self.HeaderLayout.addWidget(self.commitTimeLabel)

        if show_hash:
            self.HeaderLayout.addWidget(self.buildHashLabel)

        self.HeaderLayout.addStretch()

        # Final layout
        self.layout.addWidget(self.HeaderWidget)
        self.layout.addWidget(self.PlaceholderWidget)
        self.layout.addWidget(self.list_widget)

        self.sorting_type = SortingType(get_list_sorting_type(self.name))
        self.set_sorting_type(self.sorting_type)

    def set_info_label_text(self, text):
        self.InfoLabel.setText(text)

    def set_sorting_type(self, sorting_type):
        self.sorting_type = sorting_type
        self.list_widget.sortItems()

        self.commitTimeLabel.setChecked(False)
        self.subversionLabel.setChecked(False)

        if sorting_type == SortingType.DATETIME:
            self.commitTimeLabel.setChecked(True)
        elif sorting_type == SortingType.VERSION:
            self.subversionLabel.setChecked(True)

        set_list_sorting_type(self.name, sorting_type)
