from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton


class LeftIconButtonWidget(QPushButton):
    def __init__(self, text, icon=None):
        super().__init__()
        self.setText(" ")

        if icon is not None:
            self.setIcon(icon)

        self.setStyleSheet("text-align:left; padding-left: 4px;")
        self.setLayout(QHBoxLayout())

        label = QLabel(text)
        label.setStyleSheet("padding-left: -4px;")
        label.setAlignment(Qt.AlignCenter)
        label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.layout().addWidget(label)
