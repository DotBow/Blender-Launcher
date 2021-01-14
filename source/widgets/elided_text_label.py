from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLabel


class ElidedTextLabel(QLabel):
    def __init__(self, text=""):
        super(ElidedTextLabel, self).__init__(None)
        self.text = text

    def _setText(self, text):
        self.text = text
        self.setText(text)

    def setElidedText(self):
        metrics = QFontMetrics(self.font())
        width = self.width() - 2
        clippedText = metrics.elidedText(self.text, Qt.ElideRight, width)
        self.setText(clippedText)

    def resizeEvent(self, event):
        self.setElidedText()
