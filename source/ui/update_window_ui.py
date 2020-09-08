import resources_rc
from PyQt5.QtCore import QMetaObject, QSize, Qt
from PyQt5.QtWidgets import QProgressBar, QSizePolicy, QVBoxLayout, QWidget


class UpdateWindowUI(object):
    def setupUi(self, UpdateWindow):
        UpdateWindow.setWindowModality(Qt.ApplicationModal)
        UpdateWindow.resize(256, 64)
        UpdateWindow.setMinimumSize(QSize(256, 64))
        self.CentralWidget = QWidget(UpdateWindow)
        self.CentralLayout = QVBoxLayout(self.CentralWidget)
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        UpdateWindow.setCentralWidget(self.CentralWidget)
        QMetaObject.connectSlotsByName(UpdateWindow)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setAlignment(Qt.AlignCenter)

        self.CentralLayout.addWidget(self.ProgressBar)

    def set_progress_bar(self, value, format):
        self.ProgressBar.setFormat(format)
        self.ProgressBar.setValue(value * 100)
