# Contents of /AshitaV4Ui/AshitaV4Ui/src/Main.py

import sys
import requests
import zipfile
import configparser
import os
import shutil
from qtpy import QtWidgets
from qtpy.QtCore import QThread, Signal
from ini_data import ini_structure, tooltips, friendly_names  # Add friendly_names to import

# Worker thread to handle the download in the background
class DownloadThread(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url, dest_path, timeout=10, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.url = url
        self.dest_path = dest_path
        self.timeout = timeout

    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            with open(self.dest_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            self.finished.emit(self.dest_path)
        except Exception as e:
            self.error.emit(str(e))


class IniEditorDialog(QtWidgets.QDialog):
    def __init__(self, ini_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit INI File")
        self.ini_path = ini_path

        self.text_edit = QtWidgets.QTextEdit(self)
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

        if os.path.exists(self.ini_path):
            with open(self.ini_path, "r") as f:
                self.text_edit.setPlainText(f.read())

        self.save_button.clicked.connect(self.save_ini)
        self.cancel_button.clicked.connect(self.reject)

    def save_ini(self):
        try:
            with open(self.ini_path, "w") as f:
                f.write(self.text_edit.toPlainText())
            QtWidgets.QMessageBox.information(self, "Saved", "INI file saved successfully.")
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save INI file:\n{e}")


class NewIniDialog(QtWidgets.QDialog):
    def __init__(self, ini_dir, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New INI")
        self.ini_dir = ini_dir

        self.ini_structure = ini_structure
        self.tooltips = tooltips
        self.inputs = {}

        layout = QtWidgets.QVBoxLayout(self)

        # Filename input
        filename_layout = QtWidgets.QHBoxLayout()
        filename_layout.addWidget(QtWidgets.QLabel("Filename:"))
        self.filename_edit = QtWidgets.QLineEdit("myprofile.ini")
        filename_layout.addWidget(self.filename_edit)
        layout.addLayout(filename_layout)

        # Tabs for each section, each with a scroll area
        self.tabs = QtWidgets.QTabWidget()
        for section, keys in self.ini_structure.items():
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            tab_content = QtWidgets.QWidget()
            tab_layout = QtWidgets.QFormLayout(tab_content)
            self.inputs[section] = {}
            for key, default in keys.items():
                # Use friendly name if available, else fallback to key
                label_text = friendly_names.get(section, {}).get(key, key)
                label = QtWidgets.QLabel(label_text)
                edit = QtWidgets.QLineEdit(default)
                tooltip = self.tooltips.get(section, {}).get(key, "")
                label.setToolTip(tooltip)
                edit.setToolTip(tooltip)
                self.inputs[section][key] = edit
                tab_layout.addRow(label, edit)
            scroll.setWidget(tab_content)
            self.tabs.addTab(scroll, section)
        layout.addWidget(self.tabs)

        # Save/Cancel buttons
        btns = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Save")
        cancel_btn = QtWidgets.QPushButton("Cancel")
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)

        save_btn.clicked.connect(self.save_ini)
        cancel_btn.clicked.connect(self.reject)

        self.setLayout(layout)

    def save_ini(self):
        filename = self.filename_edit.text().strip()
        if not filename:
            QtWidgets.QMessageBox.warning(self, "Error", "Filename cannot be empty.")
            return
        if not filename.lower().endswith(".ini"):
            filename += ".ini"
        ini_path = os.path.join(self.ini_dir, filename)
        if os.path.exists(ini_path):
            QtWidgets.QMessageBox.warning(self, "Error", f"{ini_path} already exists.")
            return

        config = configparser.ConfigParser()
        for section, keys in self.inputs.items():
            config[section] = {}
            for key, edit in keys.items():
                config[section][key] = edit.text()
        try:
            with open(ini_path, "w") as f:
                config.write(f)
            QtWidgets.QMessageBox.information(self, "INI Created", f"Created: {ini_path}")
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create INI:\n{e}")


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Ashita v4 UI")

        self.download_button = QtWidgets.QPushButton("Download Ashita v4")
        self.status_label = QtWidgets.QLabel("Status: Idle")
        #self.show_ini_button = QtWidgets.QPushButton("Show INI File")
        self.create_ini_button = QtWidgets.QPushButton("Create New INI")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.download_button)
        #layout.addWidget(self.show_ini_button)
        layout.addWidget(self.create_ini_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.download_button.clicked.connect(self.start_download)
        #self.show_ini_button.clicked.connect(self.show_ini_popup)
        self.create_ini_button.clicked.connect(self.create_new_ini)

    def start_download(self):
        url = "https://github.com/AshitaXI/Ashita-v4beta/archive/refs/heads/main.zip"
        dest_path = "downloaded_file.zip"

        self.download_button.setEnabled(False)
        self.status_label.setText("Status: Downloading...")

        self.thread = DownloadThread(url, dest_path)
        self.thread.finished.connect(self.download_finished)
        self.thread.error.connect(self.download_error)
        self.thread.start()

    def download_finished(self, path):
        self.status_label.setText(f"Download complete: {path}")
        self.download_button.setEnabled(True)
        extract_dir = "."
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

    def download_error(self, err_msg):
        self.status_label.setText("Download failed")
        QtWidgets.QMessageBox.critical(self, "Error", err_msg)
        self.download_button.setEnabled(True)

    #def show_ini_popup(self):
    #    ini_path = os.path.join(
    #        os.path.dirname(__file__),
    #        "Ashita-v4beta-main", "config", "boot", "example.ini"
    #    )
    #    if not os.path.exists(ini_path):
    #        QtWidgets.QMessageBox.warning(self, "INI File", f"INI file not found:\n{ini_path}")
    #        return

    #    dialog = IniEditorDialog(ini_path, self)
    #    dialog.exec_()

    def create_new_ini(self):
        ini_dir = os.path.join(
            os.path.dirname(__file__),
            "Ashita-v4beta-main", "config", "boot"
        )
        os.makedirs(ini_dir, exist_ok=True)
        dialog = NewIniDialog(ini_dir, self)
        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())