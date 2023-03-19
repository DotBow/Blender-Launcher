from shutil import rmtree

from PyQt6.QtCore import QThread, pyqtSignal


class Remover(QThread):
    started = pyqtSignal()
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path, parent=None):
        QThread.__init__(self)
        self.path = path
        self.parent = parent

    def run(self):
        self.started.emit()

        if self.parent is not None:
            while self.parent.remover_count > 0:
                QThread.msleep(250)

            self.parent.remover_count += 1

        try:
            rmtree(self.path.as_posix())
            self.finished.emit(0)
        except OSError as e:
            self.finished.emit(1)

        if self.parent is not None:
            self.parent.remover_count -= 1

        return
