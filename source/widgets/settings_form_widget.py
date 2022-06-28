from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget


class SettingsFormWidgetRow():
    def __init__(self, label, widget):
        super().__init__()
        self.label = label
        self.widget = widget

    def setEnabled(self, enabled=True):
        self.label.setEnabled(enabled)
        self.widget.setEnabled(enabled)


class SettingsFormWidget(QWidget):
    def __init__(self, label_width):
        super().__init__()

        self.layout = QFormLayout(self)
        self.layout.setContentsMargins(6, 0, 6, 0)
        self.layout.setSpacing(6)
        self.label_width = label_width

    def _addRow(self, label_text, widget, new_line=False):
        label = QLabel(label_text)
        label.setFixedWidth(self.label_width)

        if new_line:
            self.layout.addRow(label)
            self.layout.addRow(widget)
        else:
            self.layout.addRow(label, widget)

        return SettingsFormWidgetRow(label, widget)
