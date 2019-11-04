import os

from PyQt5.QtCore import QSettings


def get_library_folder():
    settings = QSettings('blender_launcher', 'settings')
    library_folder = settings.value('library_folder')

    if (not library_folder) or (not os.path.isdir(library_folder)):
        app_folder = os.path.dirname(sys.executable)
        self.settings.setValue('library_folder', app_folder)

    return library_folder


def set_library_folder(new_library_folder):
    settings = QSettings('blender_launcher', 'settings')

    if os.path.isdir(new_library_folder):
        settings.setValue('library_folder', new_library_folder)
