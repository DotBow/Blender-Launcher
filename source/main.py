import logging
import os
import sys
import tempfile
from pathlib import Path
from shutil import copyfileobj

from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication

from modules._platform import _popen, get_platform
from windows.main_window import BlenderLauncher

version = "1.9.0"
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    _format = '%(asctime)s - %(message)s'
    logging.basicConfig(filename="Blender Launcher.log", format=_format)
    logger.error("{0} - Blender Launcher {1}".format(get_platform(), version),
                 exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def main():
    if "-update" in sys.argv:
        platform = get_platform()
        temp = Path(tempfile.gettempdir())
        cwd = Path.cwd()

        if platform == 'Windows':
            bl_exe = "Blender Launcher.exe"
        elif platform == 'Linux':
            bl_exe = "Blender Launcher"

        source = (temp / bl_exe).as_posix()
        dist = (cwd / bl_exe).as_posix()

        with open(source, 'rb') as f1, open(dist, 'wb') as f2:
            copyfileobj(f1, f2)

        if platform == 'Windows':
            _popen([dist])
        elif platform == 'Linux':
            os.chmod(dist, 0o744)
            _popen('nohup "' + dist + '"')

        sys.exit(0)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationVersion(version)
    app.setQuitOnLastWindowClosed(False)

    socket = QLocalSocket()
    socket.connectToServer("blender-launcher-server")
    is_running = socket.waitForConnected()

    if not is_running:
        socket.close()
        BlenderLauncher(app, version)
        app.exec_()


if __name__ == '__main__':
    main()
