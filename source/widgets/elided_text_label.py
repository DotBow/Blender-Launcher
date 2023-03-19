from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QLabel


class ElidedTextLabel(QLabel):
    def __init__(self, text=""):
        super().__init__()
        self.text = text
        self.metrics = QFontMetrics(self.font())

    def _setText(self, text):
        self.text = text

    def setElidedText(self):
        width = self.width()
        elided_text = self.metrics.elidedText(self.text, Qt.TextElideMode.ElideRight, width)
        self.setText(elided_text)

    def resizeEvent(self, event):
        self.setElidedText()
