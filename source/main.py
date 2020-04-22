import logging
import sys
from locale import LC_ALL, setlocale

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
    logging.basicConfig(filename="BL.log", format=_format)
    logger.error(get_platform(), exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def main():
    platform = get_platform()

    if platform == 'Windows':
        setlocale(LC_ALL, 'eng_usa')
    elif platform == 'Linux':
        setlocale(LC_ALL, 'en_US.UTF-8')

    app = QApplication(sys.argv)
    BlenderLauncher(app)
    app.exec_()


if __name__ == '__main__':
    main()
