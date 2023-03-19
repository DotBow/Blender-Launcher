from pathlib import Path

from modules._platform import get_platform
from modules.settings import get_library_folder
from PyQt6.QtCore import QThread, pyqtSignal


class LibraryDrawer(QThread):
    build_found = pyqtSignal('PyQt_PyObject')
    finished = pyqtSignal()
    build_released = pyqtSignal()

    def __init__(self, folders=['stable', 'daily', 'experimental', 'bforartists', 'custom']):
        QThread.__init__(self)
        self.folders = folders
        self.builds_count = 0
        self.build_released.connect(self.handle_build_released)

    def run(self):
        library_folder = Path(get_library_folder())

        for folder in self.folders:
            path = library_folder / folder

            if path.is_dir():
                for build in path.iterdir():
                    if (path / build).is_dir():
                        self.builds_count = self.builds_count + 1
                        self.build_found.emit(folder / build)

                        # Limit build info reader threads to 5
                        while self.builds_count > 4:
                            QThread.msleep(250)

        # Wait until all builds are drawn on screen
        while self.builds_count > 0:
            QThread.msleep(250)

        self.finished.emit()
        return

    def handle_build_released(self):
        self.builds_count = self.builds_count - 1
