from PyQt5 import QtWidgets

import main_window_design


class BlenderLauncher(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
