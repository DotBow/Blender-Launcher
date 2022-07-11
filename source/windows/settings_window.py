from modules.settings import (get_check_for_new_builds_automatically,
                              get_enable_quick_launch_key_seq,
                              get_new_builds_check_frequency,
                              set_check_for_new_builds_automatically,
                              set_new_builds_check_frequency)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton,
                             QTabWidget)
from ui.settings_window_ui import Ui_SettingsWindow
from widgets.settings_window import (appearance_tab, blender_builds_tab,
                                     connection_tab, general_tab)
from widgets.tab_widget import TabWidget

from windows.base_window import BaseWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Settings")

        # Header layout
        self.HeaderLayout = QHBoxLayout()
        self.HeaderLayout.setContentsMargins(36, 0, 0, 0)
        self.HeaderLayout.setSpacing(0)
        self.CentralLayout.addLayout(self.HeaderLayout)

        self.CloseButton = QPushButton(self.parent.icon_close, "")
        self.CloseButton.setIconSize(QSize(20, 20))
        self.CloseButton.setFixedSize(36, 32)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)
        self.CloseButton.clicked.connect(self._close)
        self.HeaderLabel = QLabel("Settings")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignRight)

        # Tab Layout
        self.TabWidget = QTabWidget()
        self.TabWidget.setProperty('Center', True)
        self.CentralLayout.addWidget(self.TabWidget)

        self.GeneralTab = TabWidget(self.TabWidget, "General")
        self.GeneralTabWidget = general_tab.GeneralTabWidget(
            parent=self.parent)
        self.GeneralTab.layout().addWidget(self.GeneralTabWidget)

        self.AppearanceTab = TabWidget(self.TabWidget, "Appearance")
        self.AppearanceTabWidget = appearance_tab.AppearanceTabWidget(
            parent=self.parent)
        self.AppearanceTab.layout().addWidget(self.AppearanceTabWidget)

        self.ConnectionTab = TabWidget(self.TabWidget, "Connection")
        self.ConnectionTabWidget = connection_tab.ConnectionTabWidget()
        self.ConnectionTab.layout().addWidget(self.ConnectionTabWidget)

        self.BlenderBuildsTab = TabWidget(self.TabWidget, "Blender Builds")
        self.BlenderBuildsTabWidget = \
            blender_builds_tab.BlenderBuildsTabWidget()
        self.BlenderBuildsTab.layout().addWidget(self.BlenderBuildsTabWidget)

        self.resize(self.sizeHint())
        self.show()

    def _close(self):
        if get_enable_quick_launch_key_seq() is True:
            self.parent.setup_global_hotkeys_listener()
        elif self.parent.listener is not None:
            self.parent.listener.stop()

        if self.GeneralTabWidget.new_builds_check_settings_changed is True:
            self.GeneralTabWidget.new_builds_check_settings_changed = False
            new_builds_check_frequency = \
                self.NewBuildsCheckFrequency.value() * 60

            if get_new_builds_check_frequency() != new_builds_check_frequency:
                set_new_builds_check_frequency(new_builds_check_frequency)
                self.GeneralTabWidget.new_builds_check_settings_changed = True

            if get_check_for_new_builds_automatically() != \
                    self.CheckForNewBuildsAutomatically.isChecked():
                set_check_for_new_builds_automatically(
                    self.CheckForNewBuildsAutomatically.isChecked())
                self.GeneralTabWidget.new_builds_check_settings_changed = True

        if self.ConnectionTabWidget.con_settings_changed or \
                self.GeneralTabWidget.new_builds_check_settings_changed:
            self.parent.draw_library(clear=True)

        self.parent.settings_window = None
        self.close()
