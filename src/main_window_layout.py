from qtpy import QtWidgets

class MainWindowLayout:
    def __init__(self, parent=None):
        # Menu bar
        self.menu_bar = QtWidgets.QMenuBar(parent)
        #Tools
        self.tools_menu = self.menu_bar.addMenu("Tools")
        self.create_ini_action = QtWidgets.QAction("Create Profile", parent)
        self.download_ashita_action = QtWidgets.QAction("Download Ashita v4", parent)
        self.tools_menu.addAction(self.create_ini_action)
        self.tools_menu.addAction(self.download_ashita_action)
        #About
        self.about_action = QtWidgets.QAction("About", parent)
        self.menu_bar.addAction(self.about_action)        

        # Not Menu bar
        self.profile_launch_button = QtWidgets.QPushButton("Launch Ashita with Profile")
        self.profile_dropdown = QtWidgets.QComboBox()
        self.manage_addons_button = QtWidgets.QPushButton("Addons, Plugins, and Keybinds Manager")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setMenuBar(self.menu_bar)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(6, 0, 6, 0)

        profile_layout = QtWidgets.QHBoxLayout()
        profile_layout.setSpacing(1)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.addWidget(QtWidgets.QLabel("Select Profile:"))
        profile_layout.addWidget(self.profile_dropdown)
        self.layout.addLayout(profile_layout)
        self.layout.addWidget(self.profile_launch_button)
        self.layout.addWidget(self.manage_addons_button)