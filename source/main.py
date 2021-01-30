import logging
import sys

from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication

from modules._platform import get_platform
from windows.main_window import BlenderLauncher
from windows.update_window import BlenderLauncherUpdater

version = "1.10.0"
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
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationVersion(version)
    app.setQuitOnLastWindowClosed(False)

    if "-update" in sys.argv:
        BlenderLauncherUpdater(app=app, version=version, tag=sys.argv[-1])
        app.exec_()
        return

    socket = QLocalSocket()
    socket.connectToServer("blender-launcher-server")
    is_running = socket.waitForConnected()

    if not is_running:
        socket.close()
        BlenderLauncher(app=app, version=version)
        app.exec_()
        return


if __name__ == '__main__':
    main()
