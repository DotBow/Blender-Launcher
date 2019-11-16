import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

import main_window_design
from _platform import get_platform
import os
from settings import *
from pathlib import Path
import zipfile


class Downloader(QThread):
    progress_changed = pyqtSignal(
        'PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject')
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent, link):
        QThread.__init__(self)
        self.parent = parent
        self.link = link

    def __del__(self):
        self.wait()

    def run(self):
        blender_zip = urlopen(self.link)
        size = blender_zip.info()['Content-Length']

        library_folder = Path(get_library_folder())
        temp_folder = library_folder / ".temp"

        # Create temp directory
        if not temp_folder.is_dir():
            temp_folder.mkdir()

        temp_folder = temp_folder / self.link.split('/', -1)[-1]

        # Download
        with open(temp_folder, 'wb') as file:
            while True:
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                file.write(chunk)
                progress = os.stat(temp_folder).st_size / int(size)
                self.progress_changed.emit(
                    progress, progress * 0.5, "Downloading: %p%")

        self.platform = get_platform()

        # Extract
        if self.platform == 'Windows':
            zf = zipfile.ZipFile(temp_folder)
            version = zf.infolist()[0].filename.split('/')[0]
            uncompress_size = sum((file.file_size for file in zf.infolist()))
            extracted_size = 0

            for file in zf.infolist():
                zf.extract(file, library_folder)
                extracted_size += file.file_size
                progress = extracted_size / uncompress_size
                self.progress_changed.emit(
                    progress, progress * 0.5 + 0.5, "Extracting: %p%")

                # if not self.is_running:
                #     zf.close()
                #     shutil.rmtree(os.path.join(library_folder, version))
                #     if os.path.isdir(temp_folder):
                #         shutil.rmtree(temp_folder)
                #     self.finished.emit(None)
                #     return

            zf.close()
        elif self.platform == 'Linux':
            tar = tarfile.open(temp_folder)
            version = tar.getnames()[0].split('/')[0]
            uncompress_size = sum((member.size for member in tar.getmembers()))
            extracted_size = 0

            for member in tar.getmembers():
                tar.extract(member, path=library_folder)
                extracted_size += member.size
                progress = extracted_size / uncompress_size
                self.progress_changed.emit(
                    progress, progress * 0.5 + 0.5, "Extracting: %p%")

                # if not self.is_running:
                #     tar.close()
                #     shutil.rmtree(os.path.join(library_folder, version))
                #     if os.path.isdir(temp_folder):
                #         shutil.rmtree(temp_folder)
                #     self.finished.emit(None)
                #     return

            tar.close()

        self.finished.emit(0)
