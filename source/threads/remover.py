from shutil import rmtree

from PyQt5.QtCore import QThread, pyqtSignal


class Remover(QThread):
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        try:
            rmtree(self.path.as_posix())
            self.finished.emit(0)
        except OSError as e:
            self.finished.emit(1)

        return
