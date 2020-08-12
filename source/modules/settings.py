import sys
from pathlib import Path

from PyQt5.QtCore import QSettings, Qt

from modules._platform import get_platform

if get_platform() == 'Windows':
    import winreg


taskbar_icon_colors = {
    'White': 0,
    'Black': 1
}

taskbar_icon_paths = {
    0: ':resources/icons/tray.ico',
    1: ':resources/icons/tray_black.ico'
}


library_pages = {
    'Stable Releases': 0,
    'Daily Builds': 1,
    'Experimental Branches': 2,
    'Custom Builds': 3
}


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
    if get_platform() == 'Windows':
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')
        path = sys.executable
        _, count, _ = winreg.QueryInfoKey(key)

        for i in range(count):
            try:
                name, value, _ = winreg.EnumValue(key, i)

                if name == 'Blender Launcher':
                    if value == path:
                        return True
                    else:
                        return False
            except WindowsError:
                pass

        key.Close()
        return False
    else:
        return False


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


def get_launch_minimized_to_tray():
    return get_settings().value('launch_minimized_to_tray', type=bool)


def set_launch_minimized_to_tray(is_checked):
    settings = get_settings()
    settings.setValue('launch_minimized_to_tray', is_checked)


def get_enable_high_dpi_scaling():
    settings = get_settings()

    if settings.contains('enable_high_dpi_scaling'):
        return get_settings().value('enable_high_dpi_scaling', type=bool)
    else:
        return True


def set_enable_high_dpi_scaling(is_checked):
    settings = get_settings()
    settings.setValue('enable_high_dpi_scaling', is_checked)


def get_default_library_page():
    settings = get_settings()

    if settings.contains('default_library_page'):
        return get_settings().value('default_library_page', type=int)
    else:
        return 0


def set_default_library_page(page):
    settings = get_settings()
    settings.setValue('default_library_page', library_pages[page])


def get_taskbar_icon_color():
    settings = get_settings()

    if settings.contains('taskbar_icon_color'):
        return get_settings().value('taskbar_icon_color', type=int)
    else:
        return 0


def set_taskbar_icon_color(color):
    settings = get_settings()
    settings.setValue('taskbar_icon_color', taskbar_icon_colors[color])


def get_list_sorting_type(list_name):
    settings = get_settings()

    if settings.contains(list_name + "_sorting_type"):
        return settings.value(list_name + "_sorting_type", type=int)
    else:
        return 1


def set_list_sorting_type(list_name, sorting_type):
    settings = get_settings()
    settings.setValue(list_name + "_sorting_type", sorting_type.value)
