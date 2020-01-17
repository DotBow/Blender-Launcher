import sys

from PyQt5.QtWidgets import QApplication

from main_window import BlenderLauncher


def main():
    app = QApplication(sys.argv)
    window = BlenderLauncher()
    app.exec_()


if __name__ == '__main__':
    main()
