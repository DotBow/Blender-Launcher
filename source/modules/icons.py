import resources_rc
from PyQt6.QtGui import QIcon, QPixmap, QColor


base_path = ":resources/icons/"


def get_icons(parent, color=QColor(255, 255, 255, 255)):
    parent.icon_settings = load_icon(color, "settings")
    parent.icon_wiki = load_icon(color, "wiki")
    parent.icon_minimize = load_icon(color, "minimize")
    parent.icon_close = load_icon(color, "close")
    parent.icon_folder = load_icon(color, "folder")
    parent.icon_favorite = load_icon(color, "favorite")
    parent.icon_fake = load_icon(color, "fake")
    parent.icon_delete = load_icon(color, "delete")
    parent.filled_circle = load_icon(color, "filled_circle")
    parent.icon_quick_launch = load_icon(color, "quick_launch")
    parent.icon_download = load_icon(color, "download")
    parent.icon_file = load_icon(color, "file")
    parent.icon_taskbar = QIcon(base_path + "bl/bl.ico")


def load_icon(color, name):
    pixmap = QPixmap(base_path + name + "")
    image = pixmap.toImage()

    for y in range(image.height()):
        for x in range(image.height()):
            color.setAlpha(image.pixelColor(x, y).alpha())
            image.setPixelColor(x, y, color)

    pixmap = QPixmap.fromImage(image)
    return QIcon(pixmap)
