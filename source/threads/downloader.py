import os
from pathlib import Path

from modules.settings import get_library_folder
from PyQt5.QtCore import QThread, pyqtSignal


class Downloader(QThread):
    started = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, manager, link):
        QThread.__init__(self)
        self.manager = manager
        self.link = link

    def run(self):
        self.started.emit()

        request = self.manager.request(
            'GET', self.link, preload_content=False)
        temp_folder = Path(get_library_folder()) / ".temp"

        # Create temp directory
        if not temp_folder.is_dir():
            temp_folder.mkdir()

        dist = temp_folder / Path(self.link).name

        # Download
        with open(dist, 'wb') as file:
            size = int(request.headers['Content-Length'])

            for chunk in request.stream(16 * 1024):
                file.write(chunk)
                progress = os.stat(dist).st_size / size
                self.progress_changed.emit(progress, "Downloading: %p%")

        request.release_conn()
        request.close()

        self.finished.emit(dist)
        return
