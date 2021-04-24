import abc
import re
import webbrowser

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QWidget

from widgets.base_menu_widget import BaseMenuWidget


class BaseBuildWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.menu = BaseMenuWidget()
        self.menu.setFont(self.parent.font)

        self.showReleaseNotesAction = QAction("Show Release Notes")
        self.showReleaseNotesAction.triggered.connect(self.show_release_notes)

    @abc.abstractmethod
    def context_menu(self):
        pass

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.list_widget.resize_signal.emit()
        return super().resizeEvent(a0)

    def set_indent(self, indent):
        self.subversionLabel.setIndent(indent)

    @QtCore.pyqtSlot()
    def show_release_notes(self):

        if self.build_info.branch == "stable":
            # TODO Check format for Blender 3 release
            # Extract X.X format version
            ver = re.search(r'\d.\d+', self.build_info.subversion).group(0)

            webbrowser.open(
                "https://wiki.blender.org/wiki/Reference/Release_Notes/{0}".format(ver))
        elif self.build_info.branch == "lts":
            # Raw numbers from version
            ver = re.sub(r'\D', '', self.build_info.subversion)

            webbrowser.open(
                "https://www.blender.org/download/lts/#lts-release-{0}".format(ver))
