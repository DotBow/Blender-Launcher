from time import strptime

from PyQt5.QtWidgets import QListWidgetItem


class BaseListWidgetItem(QListWidgetItem):
    def __init__(self, date=None):
        super().__init__()
        self.date = date

    def __lt__(self, other):
        a = strptime(self.date, "%d-%b-%H:%M")
        b = strptime(other.date, "%d-%b-%H:%M")
        return a > b
