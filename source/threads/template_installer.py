from pathlib import Path
from re import match
from shutil import copytree

from PyQt5.QtCore import QThread, pyqtSignal
from modules.settings import get_library_folder


class TemplateInstaller(QThread):
    started = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    finished = pyqtSignal()

    def __init__(self, manager, dist):
        QThread.__init__(self)
        self.manager = manager
        self.dist = dist

    def run(self):
        self.progress_changed.emit(0, "Copying Data...")
        library_folder = Path(get_library_folder())
        source = (library_folder / 'template').as_posix()

        for dir in self.dist.iterdir():
            dist = dir.as_posix()

            if match(r'\d+\.\d+.', dist) is not None:
                copytree(source, dist, dirs_exist_ok=True)
                self.finished.emit()
                return

        self.finished.emit()
        return
