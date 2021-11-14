import sys
from pathlib import Path

from PyQt5.QtCore import QSettings

from modules._platform import get_cwd, get_platform

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

tabs = {
    'Library': 0,
    'Downloads': 1,
    'User': 2
}

library_pages = {
    'Stable Releases': 0,
    'Daily Builds': 1,
    'Experimental Branches': 2
}


downloads_pages = {
    'Stable Releases': 0,
    'Daily Builds': 1,
    'Experimental Branches': 2
}


favorite_pages = {
    'Disable': 0,
    'Stable Releases': 1,
    'Daily Builds': 2,
    'Experimental Branches': 3
}


library_subfolders = [
    'custom',
    'stable',
    'daily',
    'experimental',
    'template'
]


proxy_types = {
    'None': 0,
    'HTTP': 1,
    'HTTPS': 2,
    'SOCKS4': 3,
    'SOCKS5': 4
}


def get_settings():
    return QSettings('blender_launcher', 'settings')


def get_library_folder():
    settings = get_settings()
    library_folder = settings.value('library_folder')

    if not is_library_folder_valid(library_folder):
        library_folder = get_cwd()
        settings.setValue('library_folder', library_folder)

    return library_folder


def is_library_folder_valid(library_folder=None):
    if library_folder is None:
        library_folder = get_settings().value('library_folder')

    if (library_folder is not None) and Path(library_folder).exists():
        try:
            (Path(library_folder) / ".temp").mkdir(parents=True, exist_ok=True)
        except PermissionError:
            return False

        return True
    else:
        return False


def set_library_folder(new_library_folder):
    settings = get_settings()

    if is_library_folder_valid(new_library_folder) is True:
        settings.setValue('library_folder', new_library_folder)
        create_library_folders(new_library_folder)
        return True

    return False


def create_library_folders(library_folder):
    for subfolder in library_subfolders:
        (Path(library_folder) / subfolder).mkdir(parents=True, exist_ok=True)


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
    get_settings().setValue('launch_minimized_to_tray', is_checked)


def get_enable_high_dpi_scaling():
    settings = get_settings()

    if settings.contains('enable_high_dpi_scaling'):
        return settings.value('enable_high_dpi_scaling', type=bool)
    else:
        return True


def set_enable_high_dpi_scaling(is_checked):
    get_settings().setValue('enable_high_dpi_scaling', is_checked)


def get_sync_library_and_downloads_pages():
    settings = get_settings()

    if settings.contains('sync_library_and_downloads_pages'):
        return settings.value('sync_library_and_downloads_pages', type=bool)
    else:
        return True


def set_sync_library_and_downloads_pages(is_checked):
    get_settings().setValue('sync_library_and_downloads_pages', is_checked)


def get_default_library_page():
    settings = get_settings()

    if settings.contains('default_library_page'):
        return settings.value('default_library_page', type=int)
    else:
        return 0


def set_default_library_page(page):
    get_settings().setValue('default_library_page', library_pages[page])


def get_mark_as_favorite():
    settings = get_settings()

    if settings.contains('mark_as_favorite'):
        return settings.value('mark_as_favorite', type=int)
    else:
        return 0


def set_mark_as_favorite(page):
    get_settings().setValue('mark_as_favorite', favorite_pages[page])


def get_default_downloads_page():
    settings = get_settings()

    if settings.contains('default_downloads_page'):
        return settings.value('default_downloads_page', type=int)
    else:
        return 0


def set_default_downloads_page(page):
    get_settings().setValue('default_downloads_page', downloads_pages[page])


def get_default_tab():
    settings = get_settings()

    if settings.contains('default_tab'):
        return settings.value('default_tab', type=int)
    else:
        return 0


def set_default_tab(tab):
    get_settings().setValue('default_tab', tabs[tab])


def get_taskbar_icon_color():
    settings = get_settings()

    if settings.contains('taskbar_icon_color'):
        return settings.value('taskbar_icon_color', type=int)
    else:
        return 0


def set_taskbar_icon_color(color):
    get_settings().setValue('taskbar_icon_color', taskbar_icon_colors[color])


def get_list_sorting_type(list_name):
    settings = get_settings()

    if settings.contains(list_name + "_sorting_type"):
        return settings.value(list_name + "_sorting_type", type=int)
    else:
        return 1


def set_list_sorting_type(list_name, sorting_type):
    get_settings().setValue(list_name + "_sorting_type", sorting_type.value)


def get_enable_new_builds_notifications():
    settings = get_settings()

    if settings.contains('enable_new_builds_notifications'):
        return settings.value(
            'enable_new_builds_notifications', type=bool)
    else:
        return True


def set_enable_new_builds_notifications(is_checked):
    get_settings().setValue('enable_new_builds_notifications', is_checked)


def get_enable_download_notifications():
    settings = get_settings()

    if settings.contains('enable_download_notifications'):
        return settings.value('enable_download_notifications', type=bool)
    else:
        return True


def set_enable_download_notifications(is_checked):
    get_settings().setValue('enable_download_notifications', is_checked)


def get_blender_startup_arguments():
    args = get_settings().value('blender_startup_arguments')

    if args is None:
        return ""
    else:
        return args.strip()


def set_blender_startup_arguments(args):
    get_settings().setValue('blender_startup_arguments', args.strip())


def get_bash_arguments():
    args = get_settings().value('bash_arguments')

    if args is None:
        return ""
    else:
        return args.strip()


def set_bash_arguments(args):
    get_settings().setValue('bash_arguments', args.strip())


def get_install_template():
    return get_settings().value('install_template', type=bool)


def set_install_template(is_checked):
    get_settings().setValue('install_template', is_checked)


def get_show_tray_icon():
    settings = get_settings()

    if settings.contains('show_tray_icon'):
        return settings.value('show_tray_icon', type=bool)
    else:
        return True


def set_show_tray_icon(is_checked):
    get_settings().setValue('show_tray_icon', is_checked)


def get_launch_blender_no_console():
    return get_settings().value('launch_blender_no_console', type=bool)


def set_launch_blender_no_console(is_checked):
    get_settings().setValue('launch_blender_no_console', is_checked)


def get_quick_launch_key_seq():
    key_seq = get_settings().value('quick_launch_key_seq')

    if key_seq is None:
        return "alt+f11"
    else:
        return key_seq.strip()


def set_quick_launch_key_seq(key_seq):
    get_settings().setValue('quick_launch_key_seq', key_seq.strip())


def get_enable_quick_launch_key_seq():
    settings = get_settings()

    if settings.contains('enable_quick_launch_key_seq'):
        return settings.value('enable_quick_launch_key_seq', type=bool)
    else:
        return False


def set_enable_quick_launch_key_seq(is_checked):
    get_settings().setValue('enable_quick_launch_key_seq', is_checked)


def get_proxy_type():
    settings = get_settings()

    if settings.contains('proxy_type'):
        return settings.value('proxy_type', type=int)
    else:
        return 0


def set_proxy_type(type):
    get_settings().setValue('proxy_type', proxy_types[type])


def get_proxy_host():
    host = get_settings().value('proxy_host')

    if host is None:
        return "255.255.255.255"
    else:
        return host.strip()


def set_proxy_host(args):
    get_settings().setValue('proxy_host', args.strip())


def get_proxy_port():
    port = get_settings().value('proxy_port')

    if port is None:
        return "99999"
    else:
        return port.strip()


def set_proxy_port(args):
    get_settings().setValue('proxy_port', args.strip())


def get_proxy_user():
    user = get_settings().value('proxy_user')

    if user is None:
        return ""
    else:
        return user.strip()


def set_proxy_user(args):
    get_settings().setValue('proxy_user', args.strip())


def get_proxy_password():
    password = get_settings().value('proxy_password')

    if password is None:
        return ""
    else:
        return password.strip()


def set_proxy_password(args):
    get_settings().setValue('proxy_password', args.strip())


def get_use_custom_tls_certificates():
    settings = get_settings()

    if settings.contains('use_custom_tls_certificates'):
        return settings.value('use_custom_tls_certificates', type=bool)
    else:
        return True


def set_use_custom_tls_certificates(is_checked):
    get_settings().setValue('use_custom_tls_certificates', is_checked)
