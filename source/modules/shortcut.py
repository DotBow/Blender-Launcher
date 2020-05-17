from pathlib import Path

from modules.settings import *

if get_platform() == 'Windows':
    import win32com.client
    from win32com.shell import shell, shellcon


def create_shortcut(path, name, icon):
    desktop = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
    _WSHELL = win32com.client.Dispatch("Wscript.Shell")
    dist = Path(desktop) / (name + ".lnk")
    wscript = _WSHELL.CreateShortCut(dist.as_posix())
    wscript.Targetpath = path
    wscript.WorkingDirectory = path
    wscript.WindowStyle = 0
    print(icon)
    wscript.IconLocation = icon
    wscript.save()
