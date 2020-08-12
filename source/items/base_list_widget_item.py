import re
from time import strptime

from PyQt5.QtWidgets import QListWidgetItem


class BaseListWidgetItem(QListWidgetItem):
    def __init__(self, date=None):
        super().__init__()
        self.date = date

    def __lt__(self, other):
        soring_type = self.listWidget().parent.sorting_type

        if soring_type.name == 'DATETIME':
            return self.compare_datetime(other)
        elif soring_type.name == 'VERSION':
            return self.compare_version(other)

    def compare_datetime(self, other):
        if (self.date is None) or (other.date is None):
            return False
        else:
            this_datetime = strptime(self.date, "%d-%b-%y-%H:%M")
            other_datetime = strptime(other.date, "%d-%b-%y-%H:%M")

            return this_datetime > other_datetime

    def compare_version(self, other):
        list_widget = self.listWidget()

        this_widget = list_widget.itemWidget(self)
        other_widget = list_widget.itemWidget(other)

        if (this_widget is None) or (other_widget is None):
            return False
        elif (this_widget.build_info is None) or (other_widget.build_info is None):
            return False
        else:
            this_match = re.search(
                r'\d+\.\d+', this_widget.build_info.subversion)
            other_match = re.search(
                r'\d+\.\d+', other_widget.build_info.subversion)

            this_version = float(this_match.group(0))
            other_version = float(other_match.group(0))

            if this_version == other_version:
                return self.compare_datetime(other)
            else:
                return this_version > other_version
