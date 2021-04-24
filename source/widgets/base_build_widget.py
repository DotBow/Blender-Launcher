import webbrowser
import re

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget


class BaseBuildWidget(QWidget):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.list_widget.resize_signal.emit()
        return super().resizeEvent(a0)

    def set_indent(self, indent):
        self.subversionLabel.setIndent(indent)

    @QtCore.pyqtSlot()
    def show_release_notes(self):
        # Raw numbers from version
        ver = re.sub(r'\D', '', self.build_info.subversion)

        if self.branch == "stable":
            # Example: 2-93, 2-80
            # TODO Check format for Blender 3 release
            ver = "{0}-{1}".format(ver[0], ver[1:3])

            webbrowser.open(
                "https://www.blender.org/download/releases/{0}".format(ver))
        elif self.branch == "lts":
            webbrowser.open(
                "https://www.blender.org/download/lts/#lts-release-{0}".format(ver))
