import logging
import sys

from PyQt5.QtCore import QByteArray
from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication

from modules._platform import get_platform
from windows.main_window import BlenderLauncher
from windows.update_window import BlenderLauncherUpdater

version = "1.14.0-dev"

_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=_format,
                    handlers=[
                        logging.FileHandler("Blender Launcher.log"),
                        logging.StreamHandler(stream=sys.stdout)
                    ])
logger = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("{0} - Blender Launcher {1}".format(get_platform(), version),
                 exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


help = \
    """
    Command line arguments sheet:

    -help                        * Show command line arguments sheet
    -update                      * Run updater instead of the main application
    -debug                       * Set logging level to DEBUG
    -set-library-folder "%path%" * Set library folder
    -offline                     * Disable scraper thread
    """


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationVersion(version)
    app.setQuitOnLastWindowClosed(False)

    if "-help" in sys.argv:
        print(help)
        return

    if "-update" in sys.argv:
        BlenderLauncherUpdater(app=app, version=version, tag=sys.argv[-1])
        app.exec_()
        return

    if "-debug" in sys.argv:
        logging.root.setLevel(logging.INFO)
    else:
        logging.root.setLevel(logging.DEBUG)

    socket = QLocalSocket()
    socket.connectToServer("blender-launcher-server")
    is_running = socket.waitForConnected()

    if not is_running:
        socket.close()
        BlenderLauncher(app=app, version=version,
                        argv=sys.argv, logger=logger)
        app.exec_()
        return
    else:
        socket.write(QByteArray(version.encode()))
        socket.waitForBytesWritten()


if __name__ == '__main__':
    main()
