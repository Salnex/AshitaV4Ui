import os
import sys
import zipfile
from qtpy import QtWidgets, QtCore, QtGui
from main_window_layout import MainWindowLayout
from download_thread import DownloadThread
from ini_editor_dialog import IniEditorDialog
from new_ini_dialog import NewIniDialog
from addon_plugin_manager import AddonPluginManagerWindow
from config import ASHITA_ROOT, PROJECT_ROOT, ASHITA_DOWNLOAD_URL, ASHITA_BOOT_CONFIG_DIR

def run_as_admin(exe_path, args, cwd):
    params = f'"{exe_path}" {args}'
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe_path, args, cwd, 1
        )
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Failed to elevate:\n{e}")


    
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Ashita v4 UI")

        # Use the layout class
        self.ui = MainWindowLayout(self)
        self.setLayout(self.ui.layout)
        self.setFixedSize(self.sizeHint())

        # Assign Widgets from the layout
        self.profile_launch_button = self.ui.profile_launch_button
        self.profile_dropdown = self.ui.profile_dropdown
        self.refresh_profiles()
        # Remove: self.create_ini_button = self.ui.create_ini_button
        # Remove: self.download_button = self.ui.download_button

        # Connect menu actions
        self.ui.create_ini_action.triggered.connect(self.create_new_ini)
        self.ui.download_ashita_action.triggered.connect(self.start_download)
        self.ui.about_action.triggered.connect(self.open_github_page)
        # Connect buttons
        self.profile_launch_button.clicked.connect(self.launch_ashita)
        self.ui.manage_addons_button.clicked.connect(self.open_addon_plugin_manager)
        #self.show_ini_button.clicked.connect(self.show_ini_popup)
        

    def refresh_profiles(self):
        # Find all .ini files in the config/boot directory
        print(f"Looking for INI files in: {ASHITA_BOOT_CONFIG_DIR}")
        self.profile_dropdown.clear()
        if os.path.isdir(ASHITA_BOOT_CONFIG_DIR):
            for fname in os.listdir(ASHITA_BOOT_CONFIG_DIR):
                if fname.lower().endswith(".ini"):
                    self.profile_dropdown.addItem(fname)

    def start_download(self):

        dest_path = os.path.join(PROJECT_ROOT, "ashita_download.zip")

        self.download_button.setEnabled(False)
        self.download_button.setText("Status: Downloading...")

        self.thread = DownloadThread(ASHITA_DOWNLOAD_URL, dest_path)
        self.thread.finished.connect(self.download_finished)
        self.thread.error.connect(self.download_error)
        self.thread.start()

    def download_finished(self, path):
        ##self.status_label.setText(f"Download complete: {path}")
        self.download_button.setEnabled(True)
        extract_dir = PROJECT_ROOT
        self.download_button.setText("Status: Extracting...")
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            QtWidgets.QMessageBox.information(
                self, "Download",
                f"Download completed!\nSaved to: {path}\nExtracted to: {extract_dir}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Extraction Error",
                f"Failed to extract zip file:\n{e}"
            )
        QtCore.QTimer.singleShot(250, lambda: self.download_button.setText("Download Ashita v4"))

    def download_error(self, err_msg):
        self.status_label.setText("Download failed")
        QtWidgets.QMessageBox.critical(self, "Error", err_msg)
        self.download_button.setEnabled(True)

    #def show_ini_popup(self):
    #    ini_path = os.path.join(ASHITA_ROOT, "config", "boot", "example.ini"
    #    )
    #    if not os.path.exists(ini_path):
    #        QtWidgets.QMessageBox.warning(self, "INI File", f"INI file not found:\n{ini_path}")
    #        return

    #    dialog = IniEditorDialog(ini_path, self)
    #    dialog.exec_()

    def create_new_ini(self):
        os.makedirs(ASHITA_BOOT_CONFIG_DIR, exist_ok=True)
        dialog = NewIniDialog(ASHITA_BOOT_CONFIG_DIR, self)
        dialog.exec_()
        self.refresh_profiles()

    def launch_ashita(self):
        profile = self.profile_dropdown.currentText()
        if not profile:
            QtWidgets.QMessageBox.warning(self, "No Profile", "Please select a profile to launch.")
            return
        ashita_path = os.path.join(ASHITA_ROOT, "Ashita-cli.exe")
        ini_path = os.path.join(ASHITA_BOOT_CONFIG_DIR, profile)
        if not os.path.isfile(ashita_path):
            QtWidgets.QMessageBox.critical(self, "Error", f"Ashita-cli.exe not found at:\n{ashita_path}")
            return
        if not os.path.isfile(ini_path):
            QtWidgets.QMessageBox.critical(self, "Error", f"Profile INI not found at:\n{ini_path}")
            return
        # Launch Ashita with the selected profile
        import subprocess
        try:
            if sys.platform.startswith("linux"):
                subprocess.Popen(['wine', ashita_path, profile], cwd=os.path.dirname(ashita_path))
            elif sys.platform.startswith("win"):
                run_as_admin(ashita_path, profile, os.path.dirname(ashita_path))
                QtWidgets.QMessageBox.information(self, "Launched", f"Launched Ashita with profile: {profile}")
            else:
                subprocess.Popen([ashita_path, profile], cwd=os.path.dirname(ashita_path))            
                QtWidgets.QMessageBox.information(self, "Launched", f"Launched Ashita with profile: {profile}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to launch Ashita:\n{e}")
    
    def open_addon_plugin_manager(self):
        dlg = AddonPluginManagerWindow(self)
        dlg.exec_()

    def open_github_page(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/Salnex/AshitaV4Ui"))    

    def accept(self):
        self.save_selection_to_file()
        super().accept()
