import logging
import os
import sys
import tempfile
from pathlib import Path
from shutil import copyfileobj
from subprocess import DEVNULL, Popen

from modules._platform import get_platform
from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication
from windows.main_window import BlenderLauncher

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    _format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename="Blender Launcher.log", format=_format)
    logger.error(get_platform(), exc_info=(exc_type, exc_value, exc_traceback))


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

        source = temp / bl_exe
        dist = cwd / bl_exe

        with open(source.as_posix(), 'rb') as f1, open(dist.as_posix(), 'wb') as f2:
            copyfileobj(f1, f2)

        if platform == 'Windows':
            Popen([dist.as_posix()], stdin=DEVNULL,
                  stdout=DEVNULL, stderr=DEVNULL)
        elif platform == 'Linux':
            os.chmod(dist.as_posix(), 0o744)
            Popen('nohup "' + dist.as_posix() + '"', shell=True,
                  stdout=None, stderr=None, close_fds=True)

        sys.exit(0)

    app = QApplication(sys.argv)
    app.setApplicationVersion("1.6.0")
    app.setQuitOnLastWindowClosed(False)

    socket = QLocalSocket()
    socket.connectToServer("blender-launcher-server")
    is_running = socket.waitForConnected()

    if not is_running:
        socket.close()
        BlenderLauncher(app)
        app.exec_()


if __name__ == '__main__':
    main()
