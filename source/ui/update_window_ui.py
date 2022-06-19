from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QVBoxLayout,
                             QWidget)


class UpdateWindowUI(object):
    def setupUi(self, UpdateWindow):
        UpdateWindow.setWindowModality(Qt.ApplicationModal)
        UpdateWindow.resize(256, 77)
        self.setWindowTitle("Updating Blender Launcher")

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

    def set_progress_bar(self, obtained, total):
        self.ProgressBar.setValue(obtained / total * 100)
