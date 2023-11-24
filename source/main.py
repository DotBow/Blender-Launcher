import logging
import sys

from PyQt5.QtCore import QByteArray
from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication

from modules._platform import get_cwd, get_platform
from windows.main_window import BlenderLauncher
from windows.update_window import BlenderLauncherUpdater

version = "1.15.2"

# Setup logging config
_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=_format,
                    handlers=[
                        logging.FileHandler(
                            (get_cwd() / "Blender Launcher.log")),
                        logging.StreamHandler(stream=sys.stdout)
                    ])
logger = logging.getLogger(__name__)


# Setup exception handling
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("{0} - Blender Launcher {1}".format(get_platform(), version),
                 exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


# List of available line arguments
help = \
    """
    Command line arguments sheet:

    -help                        * Show command line arguments sheet
    -update                      * Run updater instead of the main application
    -debug                       * Set logging level to DEBUG
    -set-library-folder "%path%" * Set library folder
    -offline                     * Disable scraper thread
    -instanced                   * Do not check if other BL instance is
                                   running, used for restarting app
    """


def main():
    # Create an instance of application and set its core properties
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationVersion(version)
    app.setQuitOnLastWindowClosed(False)

    # Show list of available line arguments and exit
    if "-help" in sys.argv:
        print(help)
        sys.exit()

    # Set logging level, default is 'WARNING'
    if "-debug" in sys.argv:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.WARNING)

    # Run updater instead of the main application and exit
    if "-update" in sys.argv:
        BlenderLauncherUpdater(app=app, version=version,
                               release_tag=sys.argv[-1])
        sys.exit(app.exec_())

    # Do not check for other instances running
    if "-instanced" in sys.argv:
        BlenderLauncher(app=app, version=version,
                        argv=sys.argv, logger=logger)
        sys.exit(app.exec_())

    # Check if other instances of application is already running
    socket = QLocalSocket()
    socket.connectToServer("blender-launcher-server")
    is_running = socket.waitForConnected()

    if not is_running:
        socket.close()
        BlenderLauncher(app=app, version=version,
                        argv=sys.argv, logger=logger)
        sys.exit(app.exec_())
    else:
        socket.write(QByteArray(version.encode()))
        socket.waitForBytesWritten()

    sys.exit()


if __name__ == '__main__':
    main()
