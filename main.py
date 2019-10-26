import sys

from PyQt5 import QtWidgets

from main_window import BlenderLauncher


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = BlenderLauncher()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
