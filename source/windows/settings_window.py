from modules.settings import (get_check_for_new_builds_automatically,
                              get_enable_quick_launch_key_seq,
                              get_builds_check_time, get_proxy_host,
                              get_proxy_password, get_proxy_port,
                              get_proxy_type, get_proxy_user,
                              get_quick_launch_key_seq,
                              get_use_custom_tls_certificates, proxy_types)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton,
                             QTabWidget)
from ui.settings_window_ui import Ui_SettingsWindow
from widgets.settings_window import (appearance_tab, blender_builds_tab,
                                     connection_tab, general_tab)
from widgets.tab_widget import TabWidget

from windows.base_window import BaseWindow
from windows.dialog_window import DialogWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Settings")

        # Global scope for breaking settings
        self.old_enable_quick_launch_key_seq = get_enable_quick_launch_key_seq()
        self.old_quick_launch_key_seq = get_quick_launch_key_seq()

        self.old_use_custom_tls_certificates = get_use_custom_tls_certificates()
        self.old_proxy_type = get_proxy_type()
        self.old_proxy_host = get_proxy_host()
        self.old_proxy_port = get_proxy_port()
        self.old_proxy_user = get_proxy_user()
        self.old_proxy_password = get_proxy_password()

        self.old_check_for_new_builds_automatically = \
            get_check_for_new_builds_automatically()
        self.old_new_builds_check_frequency = get_builds_check_time()

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
        self.HeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignmentFlag.AlignRight)

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
        self.pending_to_restart = []

        """Update quick launch key"""
        enable_quick_launch_key_seq = get_enable_quick_launch_key_seq()
        quick_launch_key_seq = get_quick_launch_key_seq()

        # Quick launch was enabled or disabled
        if self.old_enable_quick_launch_key_seq != enable_quick_launch_key_seq:
            # Restart hotkeys listener
            if enable_quick_launch_key_seq is True:
                self.parent.setup_global_hotkeys_listener()
            # Stop hotkeys listener
            elif self.parent.listener is not None:
                self.parent.listener.stop()
        # Only key sequence was changed
        elif self.old_quick_launch_key_seq != quick_launch_key_seq:
            # Restart hotkeys listener
            if enable_quick_launch_key_seq is True:
                self.parent.setup_global_hotkeys_listener()

        """Update connection"""
        use_custom_tls_certificates = get_use_custom_tls_certificates()
        proxy_type = get_proxy_type()
        proxy_host = get_proxy_host()
        proxy_port = get_proxy_port()
        proxy_user = get_proxy_user()
        proxy_password = get_proxy_password()

        # Restart app if any of the connection settings changed
        if self.old_use_custom_tls_certificates != use_custom_tls_certificates:
            self.pending_to_restart.append("Use Custom TLS Certificates: {}🠆{}".format(
                "ON" if self.old_use_custom_tls_certificates else "OFF",
                "ON" if use_custom_tls_certificates else "OFF"))

        if self.old_proxy_type != proxy_type:
            r_proxy_types = dict(zip(proxy_types.values(), proxy_types.keys()))

            self.pending_to_restart.append("Proxy Type: {}🠆{}".format(
                r_proxy_types[self.old_proxy_type], r_proxy_types[proxy_type]))

        if self.old_proxy_host != proxy_host:
            self.pending_to_restart.append("Proxy Host: {}🠆{}".format(
                self.old_proxy_host, proxy_host))

        if self.old_proxy_port != proxy_port:
            self.pending_to_restart.append("Proxy Port: {}🠆{}".format(
                self.old_proxy_port, proxy_port))

        if self.old_proxy_user != proxy_user:
            self.pending_to_restart.append("Proxy User: {}🠆{}".format(
                self.old_proxy_user, proxy_user))

        if self.old_proxy_password != proxy_password:
            self.pending_to_restart.append("Proxy Password")

        """Update build check frequency"""
        check_for_new_builds_automatically = \
            get_check_for_new_builds_automatically()
        new_builds_check_frequency = get_builds_check_time()

        # Restart scraper if any of the build check settings changed
        if self.old_check_for_new_builds_automatically != \
                check_for_new_builds_automatically or \
                self.old_new_builds_check_frequency != \
                new_builds_check_frequency:
            self.parent.draw_library(clear=True)

        """Ask for app restart if needed else destroy self"""
        if len(self.pending_to_restart) != 0:
            self.show_dlg_restart_bl()
        else:
            self._destroy()

    def show_dlg_restart_bl(self):
        pending_to_restart = ""

        for str in self.pending_to_restart:
            pending_to_restart += "<br>- " + str

        self.dlg = DialogWindow(
            parent=self.parent, title="Warning",
            text="Restart Blender Launcher in<br> \
                  order to apply following settings:{}".
            format(pending_to_restart),
            accept_text="Restart Now", cancel_text="Ignore")
        self.dlg.accepted.connect(self.restart_app)
        self.dlg.cancelled.connect(self._destroy)

    def restart_app(self):
        self.parent.restart_app()

    def _destroy(self):
        self.parent.settings_window = None
        self.close()
