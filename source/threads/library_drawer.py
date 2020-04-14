from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import get_platform
from modules.settings import *


class LibraryDrawer(QThread):
    build_found = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def run(self):
        library_folder = Path(get_library_folder())

        if get_platform() == 'Windows':
            blender_exe = "blender.exe"
        elif get_platform() == 'Linux':
            blender_exe = "blender"

        for dir in library_folder.iterdir():
            for build in dir.iterdir():
                path = library_folder / dir / build / blender_exe

                if path.is_file():
                    self.build_found.emit(dir / build, dir.name)

        return
