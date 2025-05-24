# Contents of /AshitaV4Ui/AshitaV4Ui/src/Main.py

import sys
import requests
import zipfile
import configparser
import os
import shutil
from qtpy import QtWidgets
from qtpy.QtCore import QThread, Signal
from ini_data import ini_structure, tooltips, friendly_names, valid_values, hidden_keys, padmode000_options, padsin000_options

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

        # Prepare a special tab for gamepad options
        gamepad_tab = QtWidgets.QWidget()
        gamepad_layout = QtWidgets.QFormLayout(gamepad_tab)
        gamepad_inputs = {}

        for section, keys in self.ini_structure.items():
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            tab_content = QtWidgets.QWidget()
            tab_layout = QtWidgets.QFormLayout(tab_content)
            self.inputs[section] = {}
            for key, default in keys.items():
                # Skip hidden keys
                if key in hidden_keys.get(section, set()):
                    continue
                label_text = friendly_names.get(section, {}).get(key, key)
                tooltip = self.tooltips.get(section, {}).get(key, "")
                # Use dropdown if valid values exist
                valid = valid_values.get(section, {}).get(key)

                # Move gamepad options to the special tab
                if section == "ffxi.registry" and key == "padmode000":
                    groupbox = QtWidgets.QGroupBox(label_text)
                    vbox = QtWidgets.QVBoxLayout(groupbox)
                    checkboxes = []
                    # Default is a comma-separated string, e.g. "1,0,1,0,1,1"
                    default_values = [x.strip() for x in default.split(",")] if default else ["0"] * 6
                    for i, (opt_label, opt_tip) in enumerate(padmode000_options):
                        cb = QtWidgets.QCheckBox(opt_label)
                        cb.setToolTip(opt_tip)
                        if i < len(default_values) and default_values[i] == "1":
                            cb.setChecked(True)
                        vbox.addWidget(cb)
                        checkboxes.append(cb)
                    groupbox.setToolTip(tooltip)
                    gamepad_inputs[key] = checkboxes
                    gamepad_layout.addRow(groupbox)
                    continue
                elif section == "ffxi.registry" and key == "padsin000":
                    groupbox = QtWidgets.QGroupBox(label_text)
                    vbox = QtWidgets.QVBoxLayout(groupbox)
                    spinboxes = []
                    # Default is a comma-separated string, e.g. "0,1,2,..."
                    default_values = [x.strip() for x in default.split(",")] if default else ["0"] * 27
                    for i, (desc, tip) in enumerate(padsin000_options):
                        hbox = QtWidgets.QHBoxLayout()
                        label = QtWidgets.QLabel(f"{i}: {desc}")
                        label.setToolTip(tip)
                        spin = QtWidgets.QSpinBox()
                        spin.setMinimum(0)
                        spin.setMaximum(255)
                        spin.setToolTip(tip)
                        if i < len(default_values):
                            try:
                                spin.setValue(int(default_values[i]))
                            except ValueError:
                                spin.setValue(0)
                        hbox.addWidget(label)
                        hbox.addWidget(spin)
                        vbox.addLayout(hbox)
                        spinboxes.append(spin)
                    groupbox.setToolTip(tooltip)
                    gamepad_inputs[key] = spinboxes
                    gamepad_layout.addRow(groupbox)
                    continue
                elif section == "ffxi.registry" and key == "padguid000":
                    edit = QtWidgets.QLineEdit(default)
                    edit.setToolTip(tooltip)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    gamepad_inputs[key] = edit
                    gamepad_layout.addRow(label, edit)
                    continue

                # All other keys as before
                if valid:
                    combo = QtWidgets.QComboBox()
                    combo.setToolTip(tooltip)
                    # Add items as (label, value)
                    for label, value in valid.items():
                        combo.addItem(label, value)
                        # Set default if matches
                        if str(default) == str(value):
                            combo.setCurrentText(label)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    self.inputs[section][key] = combo
                    tab_layout.addRow(label, combo)
                elif "boolean" in tooltip.lower():
                    checkbox = QtWidgets.QCheckBox()
                    checkbox.setChecked(str(default).lower() in ("1", "true", "yes", "on"))
                    checkbox.setToolTip(tooltip)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    self.inputs[section][key] = checkbox
                    tab_layout.addRow(label, checkbox)
                else:
                    edit = QtWidgets.QLineEdit(default)
                    edit.setToolTip(tooltip)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    self.inputs[section][key] = edit
                    tab_layout.addRow(label, edit)
            scroll.setWidget(tab_content)
            self.tabs.addTab(scroll, section)

        # Add the gamepad tab last
        self.inputs["gamepad"] = gamepad_inputs
        self.tabs.addTab(gamepad_tab, "Gamepad")
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
        for section, keys in self.ini_structure.items():
            config[section] = {}
            # Write visible keys from UI (excluding gamepad keys)
            for key, widget in self.inputs.get(section, {}).items():
                if key in ("padmode000", "padsin000", "padguid000") and section == "ffxi.registry":
                    continue  # These are handled in the gamepad tab
                if isinstance(widget, QtWidgets.QCheckBox):
                    config[section][key] = "1" if widget.isChecked() else "0"
                elif isinstance(widget, QtWidgets.QComboBox):
                    config[section][key] = widget.currentData()
                else:
                    config[section][key] = widget.text()
            # Write hidden keys with their default values
            for key, default in keys.items():
                if key in hidden_keys.get(section, set()):
                    config[section][key] = default

        # Write gamepad tab values into ffxi.registry
        gamepad_inputs = self.inputs.get("gamepad", {})
        if "ffxi.registry" not in config:
            config["ffxi.registry"] = {}

        # padmode000: checkboxes
        padmode = gamepad_inputs.get("padmode000")
        if padmode:
            values = ["1" if cb.isChecked() else "0" for cb in padmode]
            # If all are "0" (unchecked), treat as default and write "-1"
            if all(v == "0" for v in values):
                config["ffxi.registry"]["padmode000"] = "-1"
            else:
                config["ffxi.registry"]["padmode000"] = ",".join(values)

        # padsin000: spinboxes
        padsin = gamepad_inputs.get("padsin000")
        if padsin:
            values = [str(spin.value()) for spin in padsin]
            # If all are "0", treat as default and write "-1"
            if all(v == "0" for v in values):
                config["ffxi.registry"]["padsin000"] = "-1"
            else:
                config["ffxi.registry"]["padsin000"] = ",".join(values)

        # padguid000: line edit
        padguid = gamepad_inputs.get("padguid000")
        if padguid:
            config["ffxi.registry"]["padguid000"] = padguid.text()

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