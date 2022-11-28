from enum import Enum

from modules.settings import (get_list_sorting_type, set_list_sorting_type, 
                              get_theme)
from modules.theme import Theme, theme
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget)

from widgets.base_list_widget import BaseListWidget

from darkdetect import isLight

class SortingType(Enum):
    DATETIME = 1
    VERSION = 2


class BasePageWidget(QWidget):
    def __init__(self, parent, page_name, time_label, info_text,
                 show_reload=False, extended_selection=False):
        super().__init__()
        self.name = page_name

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Placeholder Widget
        self.PlaceholderWidget = QWidget()
        self.PlaceholderWidget.setProperty("ToolBoxWidget", True)
        self.PlaceholderLayout = QVBoxLayout(self.PlaceholderWidget)
        self.PlaceholderLayout.setContentsMargins(0, 0, 0, 0)
        
        self.InfoPixmapLabel = QLabel()
        self.InfoPixmapLabel.setScaledContents(True)
        self.InfoPixmapLabel.setFixedSize(32, 32)

        self.loadInfoPixmapIcon()
        theme.changed.connect(self.loadInfoPixmapIcon)

        self.InfoLabelLayout = QHBoxLayout()
        self.InfoLabelLayout.setContentsMargins(0, 0, 0, 6)
        self.InfoLabel = QLabel(info_text)
        self.InfoLabelLayout.addWidget(self.InfoLabel)

        self.list_widget = BaseListWidget(
            self, extended_selection=extended_selection)
        self.list_widget.hide()

        self.InfoLayout = QHBoxLayout()
        self.InfoLayout.setContentsMargins(0, 0, 0, 0)

        self.InfoLayout.addStretch()
        self.InfoLayout.addWidget(self.InfoPixmapLabel)
        self.InfoLayout.addLayout(self.InfoLabelLayout)
        self.InfoLayout.addStretch()

        self.PlaceholderLayout.addStretch()
        self.PlaceholderLayout.addLayout(self.InfoLayout)

        if show_reload is True:
            self.ReloadBtn = QPushButton("Reload")
            self.ReloadBtn.setToolTip(
                "Reload Custom builds from disk")
            self.ReloadBtn.clicked.connect(parent.reload_custom_builds)

            self.ReloadBtnLayout = QHBoxLayout()
            self.ReloadBtnLayout.addStretch()
            self.ReloadBtnLayout.addWidget(self.ReloadBtn)
            self.ReloadBtnLayout.addStretch()

            self.PlaceholderLayout.addLayout(self.ReloadBtnLayout)

        self.PlaceholderLayout.addStretch()

        # Header Widget
        self.HeaderWidget = QWidget()
        self.HeaderWidget.hide()
        self.HeaderWidget.setProperty("ToolBoxWidget", True)
        self.HeaderLayout = QHBoxLayout(self.HeaderWidget)
        self.HeaderLayout.setContentsMargins(2, 0, 0, 0)
        self.HeaderLayout.setSpacing(2)

        if show_reload is True:
            self.fakeLabel = QPushButton("Reload")
            self.fakeLabel.setToolTip(
                "Reload Custom builds from disk")
            self.fakeLabel.setProperty("ListHeader", True)
            self.fakeLabel.clicked.connect(parent.reload_custom_builds)
        else:
            self.fakeLabel = QLabel()

        self.fakeLabel.setFixedWidth(85)

        self.subversionLabel = QPushButton("Version")
        self.subversionLabel.setFixedWidth(75)
        self.subversionLabel.setProperty("ListHeader", True)
        self.subversionLabel.setCheckable(True)
        self.subversionLabel.clicked.connect(
            lambda: self.set_sorting_type(SortingType.VERSION))
        self.branchLabel = QLabel("Branch")
        self.branchLabel.setAlignment(Qt.AlignCenter)
        self.commitTimeLabel = QPushButton(time_label)
        self.commitTimeLabel.setFixedWidth(118)
        self.commitTimeLabel.setProperty("ListHeader", True)
        self.commitTimeLabel.setCheckable(True)
        self.commitTimeLabel.clicked.connect(
            lambda: self.set_sorting_type(SortingType.DATETIME))

        self.HeaderLayout.addWidget(self.fakeLabel)
        self.HeaderLayout.addWidget(self.subversionLabel)
        self.HeaderLayout.addWidget(self.branchLabel, stretch=1)
        self.HeaderLayout.addWidget(self.commitTimeLabel)
        self.HeaderLayout.addSpacing(34)

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

    def loadInfoPixmapIcon(self):
        if Theme.isLight():
            self.InfoPixmap = QPixmap(":resources/icons/black/info.svg")
        else:
            self.InfoPixmap = QPixmap(":resources/icons/white/info.svg")
        
        self.InfoPixmapLabel.setPixmap(self.InfoPixmap)
