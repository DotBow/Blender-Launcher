import os
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal


class FolderObserver(QThread):
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent, folder):
        QThread.__init__(self)
        self.parent = parent
        self.folder = Path(folder)

    def run(self):
        self.started.emit()
        subfolders = self.get_subfolders()

        while self.parent:
            new_subfolders = self.get_subfolders()

            if subfolders != new_subfolders:
                if len(new_subfolders) > len(subfolders):
                    for sub in new_subfolders:
                        if sub not in subfolders:
                            print("New -> " + sub)
                elif len(new_subfolders) < len(subfolders):
                    for sub in subfolders:
                        if sub not in new_subfolders:
                            print("Deleted -> " + sub)
                else:
                    for sub in new_subfolders:
                        if sub not in subfolders:
                            print("Changed -> " + sub)

                subfolders = new_subfolders

            QThread.sleep(3)

        return

    def get_subfolders(self):
        subfolders = []

        for sub in self.folder.iterdir():
            if sub.is_dir():
                subfolders.append(sub.name)

        return subfolders
