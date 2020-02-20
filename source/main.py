import sys

from PyQt5.QtWidgets import QApplication

from windows.main_window import BlenderLauncher


def main():
    app = QApplication(sys.argv)
    window = BlenderLauncher(app)
    app.exec_()


if __name__ == '__main__':
    main()
