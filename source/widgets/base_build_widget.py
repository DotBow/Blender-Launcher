import abc
import re
import webbrowser

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget

from widgets.base_menu_widget import BaseMenuWidget


class BaseBuildWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.menu = BaseMenuWidget()
        self.menu.setFont(self.parent.font_10)

        self.showReleaseNotesAction = QAction("Show Release Notes")
        self.showReleaseNotesAction.triggered.connect(self.show_release_notes)

    @abc.abstractmethod
    def context_menu(self):
        pass

    @QtCore.pyqtSlot()
    def show_release_notes(self):
        branch = self.build_info.branch

        if branch in {"stable", "daily"}:
            # TODO Check format for Blender 3 release
            # Extract X.X format version
            ver = re.search(r'\d.\d+', self.build_info.subversion).group(0)

            webbrowser.open(
                "https://wiki.blender.org/wiki/Reference/Release_Notes/{}".format(ver))
        elif branch == "lts":
            # Raw numbers from version
            ver = re.sub(r'\D', '', self.build_info.subversion)

            webbrowser.open(
                "https://www.blender.org/download/lts/#lts-release-{}".format(ver))
        else:  # Open for builds with D12345 name pattern
            # Extract only D12345 substring
            m = re.search(r'D\d{5}', branch)

            webbrowser.open(
                "https://developer.blender.org/{}".format(m.group(0)))
