from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton


class LeftIconButtonWidget(QPushButton):
    def __init__(self, text, icon):
        super().__init__()
        self.setIcon(icon)
        self.setStyleSheet("text-align:left;")
        self.setLayout(QHBoxLayout())

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.layout().addWidget(label)
