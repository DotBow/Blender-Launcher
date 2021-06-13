from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal


class Renamer(QThread):
    started = pyqtSignal()
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, src_path, dst_name, parent=None):
        QThread.__init__(self)
        self.src_path = src_path
        self.dst_name = dst_name
        self.parent = parent

    def run(self):
        self.started.emit()

        if self.parent is not None:
            while self.parent.renamer_count > 0:
                QThread.msleep(250)

            self.parent.renamer_count += 1

        try:
            dst = Path(self.src_path).parent / self.dst_name
            self.src_path.rename(dst)
            self.finished.emit(dst)
        except OSError as e:
            self.finished.emit(None)

        if self.parent is not None:
            self.parent.remover_count -= 1

        return
