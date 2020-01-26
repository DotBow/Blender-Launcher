from pathlib import Path

from PyQt5.QtCore import QSettings


def get_library_folder():
    settings = QSettings('blender_launcher', 'settings')
    library_folder = settings.value('library_folder')

    if not Path(library_folder).exists():
        library_folder = Path.cwd()
        settings.setValue('library_folder', library_folder)

    return library_folder


def set_library_folder(new_library_folder):
    settings = QSettings('blender_launcher', 'settings')

    if Path(new_library_folder).exists():
        settings.setValue('library_folder', new_library_folder)
