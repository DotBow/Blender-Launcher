from PyQt5.QtCore import QMetaObject, QSize, Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QSizePolicy,
                             QVBoxLayout, QWidget)


class UpdateWindowUI(object):
    def setupUi(self, UpdateWindow):
        UpdateWindow.setWindowModality(Qt.ApplicationModal)
        UpdateWindow.resize(256, 77)

        self.CentralWidget = QWidget(UpdateWindow)
        self.CentralLayout = QVBoxLayout(self.CentralWidget)
        self.CentralLayout.setContentsMargins(3, 0, 3, 3)

        UpdateWindow.setCentralWidget(self.CentralWidget)

        self.HeaderLayout = QHBoxLayout()
        self.HeaderLayout.setContentsMargins(1, 5, 1, 0)
        self.HeaderLayout.setSpacing(0)

        self.HeaderLabel = QLabel("Updating Blender Launcher")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setAlignment(Qt.AlignCenter)
        self.ProgressBar.setFixedHeight(36)

        self.HeaderLayout.addWidget(self.HeaderLabel)
        self.CentralLayout.addLayout(self.HeaderLayout)
        self.CentralLayout.addWidget(self.ProgressBar)

        QMetaObject.connectSlotsByName(UpdateWindow)

    def set_progress_bar(self, value, format):
        self.ProgressBar.setFormat(format)
        self.ProgressBar.setValue(value * 100)
