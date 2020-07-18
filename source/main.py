import logging
import sys

from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtWidgets import QApplication

from modules._platform import get_platform
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
    app = QApplication(sys.argv)
    app.setApplicationVersion("v1.3.1")
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
