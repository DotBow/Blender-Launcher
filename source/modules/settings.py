from pathlib import Path

from PyQt5.QtCore import QSettings


def get_settings():
    return QSettings('blender_launcher', 'settings')


def get_library_folder():
    settings = get_settings()
    library_folder = settings.value('library_folder')

    if not Path(library_folder).exists():
        library_folder = Path.cwd()
        settings.setValue('library_folder', library_folder)

    return library_folder


def set_library_folder(new_library_folder):
    settings = get_settings()

    if Path(new_library_folder).exists():
        settings.setValue('library_folder', new_library_folder)


def get_favorite_path():
    return get_settings().value('favorite_path')


def set_favorite_path(path):
    get_settings().setValue('favorite_path', path)
