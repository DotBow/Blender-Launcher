import sys
from pathlib import Path
from shutil import copyfile

from modules._platform import *
from modules.settings import *

if get_platform() == 'Windows':
    import win32com.client
    from win32com.shell import shell, shellcon


def create_shortcut(folder, name):
    platform = get_platform()
    library_folder = Path(get_library_folder())

    if platform == 'Windows':
        targetpath = library_folder / folder / "blender.exe"
        workingdir = library_folder / folder
        desktop = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
        dist = Path(desktop) / (name + ".lnk")

        if getattr(sys, 'frozen', False):
            icon = sys._MEIPASS + "/files/winblender.ico"
        else:
            icon = Path(
                "./resources/icons/winblender.ico").resolve().as_posix()

        icon_location = library_folder / folder / "winblender.ico"
        copyfile(icon, icon_location.as_posix())

        _WSHELL = win32com.client.Dispatch("Wscript.Shell")
        wscript = _WSHELL.CreateShortCut(dist.as_posix())
        wscript.Targetpath = targetpath.as_posix()
        wscript.WorkingDirectory = workingdir.as_posix()
        wscript.WindowStyle = 0
        wscript.IconLocation = icon_location.as_posix()
        wscript.save()
    elif platform == 'Linux':
        _exec = library_folder / folder / "blender"
        icon = library_folder / folder / "blender.svg"
        desktop = Path.home() / "Desktop"
        filename = name.replace(' ', '-')
        dist = desktop / (filename + ".desktop")

        desktop_entry = \
            "[Desktop Entry]\n" + \
            "Name={0}\n".format(name) + \
            "Comment=3D modeling, animation, rendering and post-production\n" + \
            "Keywords=3d;cg;modeling;animation;painting;sculpting;texturing;video editing;video tracking;rendering;render engine;cycles;game engine;python;\n" + \
            "Icon={0}\n".format(icon.as_posix().replace(' ', r'\ ')) + \
            "Terminal=false\n" + \
            "Type=Application\n" + \
            "Categories=Graphics;3DGraphics;\n" + \
            "MimeType=application/x-blender;\n" + \
            "Exec={0} %f".format(_exec.as_posix().replace(' ', r'\ '))

        with open(dist, 'w') as file:
            file.write(desktop_entry)
