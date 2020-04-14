from time import strptime

from PyQt5.QtWidgets import QListWidgetItem


class BaseListWidgetItem(QListWidgetItem):
    def __init__(self, date=None):
        super().__init__()
        self.date = date

    def __lt__(self, other):
        if (self.date is None) or (other.date is None):
            return True
        else:
            a = strptime(self.date, "%d-%b-%y-%H:%M")
            b = strptime(other.date, "%d-%b-%y-%H:%M")
            return a > b
