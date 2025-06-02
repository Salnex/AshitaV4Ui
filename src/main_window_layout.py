from qtpy import QtWidgets

class MainWindowLayout:
    def __init__(self, parent=None):
        self.profile_launch_button = QtWidgets.QPushButton("Launch Ashita with Profile")
        self.profile_dropdown = QtWidgets.QComboBox()
        self.create_ini_button = QtWidgets.QPushButton("Create New INI")
        self.manage_addons_button = QtWidgets.QPushButton("Manage Addons & Plugins")
        self.download_button = QtWidgets.QPushButton("Download Ashita v4")
        self.layout = QtWidgets.QVBoxLayout()
        profile_layout = QtWidgets.QHBoxLayout()
        profile_layout.addWidget(QtWidgets.QLabel("Select Profile:"))
        profile_layout.addWidget(self.profile_dropdown)
        self.layout.addLayout(profile_layout)
        self.layout.addWidget(self.profile_launch_button)
        self.layout.addWidget(self.create_ini_button)
        self.layout.addWidget(self.manage_addons_button)
        self.layout.addWidget(self.download_button)