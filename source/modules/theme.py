from PyQt5.QtCore import QObject, pyqtSignal
from modules.settings import get_theme
from darkdetect import isLight

class Theme(QObject):
    changed = pyqtSignal()
    
    def __init__(self) -> None:
        super(Theme, self).__init__()

    def themeChanged(self):
        self.changed.emit()

    @staticmethod
    def isLight():
        if get_theme() == 0:
            return isLight()
        elif get_theme() == 1:
            return True
        else:
            return False

theme = Theme()