from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui


class BaseBuildWidget(QWidget):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.list_widget.resize_signal.emit()
        return super().resizeEvent(a0)

    def set_indent(self, indent):
        self.subversionLabel.setIndent(indent)
