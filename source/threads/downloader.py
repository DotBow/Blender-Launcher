import json
import os
import zipfile
from pathlib import Path
from urllib.request import urlopen

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import get_platform
from modules.settings import *


class Downloader(QThread):
    started = pyqtSignal()
    progress_changed = pyqtSignal(
        'PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject')
    finished = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, parent, build_info):
        QThread.__init__(self)
        self.parent = parent
        self.build_info = build_info

    def __del__(self):
        self.wait()

    def run(self):
        self.started.emit()
        blender_zip = urlopen(self.build_info.link)
        size = blender_zip.info()['Content-Length']

        library_folder = Path(get_library_folder())
        temp_folder = library_folder / ".temp"

        # Create temp directory
        if not temp_folder.is_dir():
            temp_folder.mkdir()

        temp_folder = temp_folder / Path(self.build_info.link).name

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

        if self.build_info.branch == 'stable':
            dist = library_folder / 'stable'
        elif self.build_info.branch == 'daily':
            dist = library_folder / 'daily'
        else:
            dist = library_folder / 'experimental'

        # Extract
        if self.platform == 'Windows':
            zf = zipfile.ZipFile(temp_folder)
            version = zf.infolist()[0].filename.split('/')[0]
            uncompress_size = sum((file.file_size for file in zf.infolist()))
            extracted_size = 0

            for file in zf.infolist():
                zf.extract(file, dist)
                extracted_size += file.file_size
                progress = extracted_size / uncompress_size
                self.progress_changed.emit(
                    progress, progress * 0.5 + 0.5, "Extracting: %p%")

            zf.close()
        elif self.platform == 'Linux':
            tar = tarfile.open(temp_folder)
            version = tar.getnames()[0].split('/')[0]
            uncompress_size = sum((member.size for member in tar.getmembers()))
            extracted_size = 0

            for member in tar.getmembers():
                tar.extract(member, path=dist)
                extracted_size += member.size
                progress = extracted_size / uncompress_size
                self.progress_changed.emit(
                    progress, progress * 0.5 + 0.5, "Extracting: %p%")

            tar.close()

        self.finished.emit(0, dist / Path(self.build_info.link).stem)
        return
