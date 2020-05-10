import sys
from pathlib import Path

from PyQt5.QtCore import QSettings, Qt

from modules._platform import get_platform

if get_platform() == 'Windows':
    import winreg


def get_settings():
    return QSettings('blender_launcher', 'settings')


def get_library_folder():
    settings = get_settings()
    library_folder = settings.value('library_folder')

    if not is_library_folder_valid():
        library_folder = Path.cwd()
        settings.setValue('library_folder', library_folder)

    return library_folder


def is_library_folder_valid():
    library_folder = get_settings().value('library_folder')

    if (library_folder is not None) and Path(library_folder).exists():
        return True
    else:
        return False


def set_library_folder(new_library_folder):
    settings = get_settings()

    if Path(new_library_folder).exists():
        settings.setValue('library_folder', new_library_folder)


def get_favorite_path():
    return get_settings().value('favorite_path')


def set_favorite_path(path):
    get_settings().setValue('favorite_path', path)


def get_launch_when_system_starts():
    return get_settings().value('launch_when_system_starts', type=bool)


def set_launch_when_system_starts(is_checked):
    if get_platform() == 'Windows':
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                             0, winreg.KEY_SET_VALUE)

        if (is_checked):
            path = sys.executable
            winreg.SetValueEx(key, 'Blender Launcher',
                              0, winreg.REG_SZ, path)
        else:
            try:
                winreg.DeleteValue(key, 'Blender Launcher')
            except Exception:
                pass

        key.Close()

    settings = get_settings()
    settings.setValue('launch_when_system_starts', is_checked)


def get_launch_minimized_to_tray():
    return get_settings().value('launch_minimized_to_tray', type=bool)


def set_launch_minimized_to_tray(is_checked):
    settings = get_settings()
    settings.setValue('launch_minimized_to_tray', is_checked)


def get_enable_high_dpi_scaling():
    return get_settings().value('enable_high_dpi_scaling', type=bool)


def set_enable_high_dpi_scaling(app, is_checked):
    if is_checked:
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        app.setAttribute(Qt.AA_DisableHighDpiScaling)

    settings = get_settings()
    settings.setValue('enable_high_dpi_scaling', is_checked)
