from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import get_platform
from modules.settings import get_library_folder


class LibraryDrawer(QThread):
    build_found = pyqtSignal('PyQt_PyObject')
    finished = pyqtSignal()

    def __init__(self, folders=['stable', 'daily', 'experimental', 'custom']):
        QThread.__init__(self)
        self.folders = folders
        self.builds_count = 0

    def run(self):
        library_folder = Path(get_library_folder())

        if get_platform() == 'Windows':
            blender_exe = "blender.exe"
        elif get_platform() == 'Linux':
            blender_exe = "blender"

        for folder in self.folders:
            path = library_folder / folder

            if path.is_dir():
                for build in path.iterdir():
                    if (path / build / blender_exe).is_file():
                        self.builds_count = self.builds_count + 1
                        self.build_found.emit(folder / build)

                        # Limit build info reader threads to 10
                        while self.builds_count > 9:
                            QThread.msleep(100)

        # Wait until all builds are drawn on screen
        while self.builds_count > 0:
            QThread.msleep(100)

        self.finished.emit()
        return

    def release_build(self):
        self.builds_count = self.builds_count - 1
