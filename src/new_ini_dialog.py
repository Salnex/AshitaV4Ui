import os
import configparser
from qtpy import QtWidgets
from ini_data import ini_structure, tooltips, friendly_names, padmode000_options, padsin000_options, ui_metadata
from config import PROFILE_NAME_DEFAULT
from GamepadButtonMapButton import GamepadButtonMapButton

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
        self.filename_edit = QtWidgets.QLineEdit(PROFILE_NAME_DEFAULT)
        filename_layout.addWidget(self.filename_edit)
        layout.addLayout(filename_layout)

        # Tabs for each section, each with a scroll area
        self.tabs = QtWidgets.QTabWidget()
        tab_widgets = {}      
        tab_inputs = {}    

        for section, keys in self.ini_structure.items():
            for key, default in keys.items():
                meta = ui_metadata.get(section, {}).get(key, {"widget": "lineedit", "show": True, "tab": section})
                if not meta.get("show", True):
                    continue
                tab_name = meta.get("tab", section)
                if tab_name not in tab_widgets:
                    scroll = QtWidgets.QScrollArea()
                    scroll.setWidgetResizable(True)
                    tab_content = QtWidgets.QWidget()
                    tab_layout = QtWidgets.QFormLayout(tab_content)
                    scroll.setWidget(tab_content)
                    self.tabs.addTab(scroll, tab_name)
                    tab_widgets[tab_name] = (scroll, tab_layout)
                    tab_inputs[tab_name] = {}
                _, tab_layout = tab_widgets[tab_name]
                if section not in tab_inputs[tab_name]:
                    tab_inputs[tab_name][section] = {}
                label_text = friendly_names.get(section, {}).get(key, key)
                tooltip = tooltips.get(section, {}).get(key, "")
                valid = meta.get("valid_values")
                widget_type = meta.get("widget", "lineedit")

                # Special handling for gamepad groups
                if widget_type == "padmode_group":
                    groupbox = QtWidgets.QGroupBox(label_text)
                    vbox = QtWidgets.QVBoxLayout(groupbox)
                    checkboxes = []
                    default_values = [x.strip() for x in default.split(",")] if default else ["0"] * 6
                    for i, (opt_label, opt_tip) in enumerate(padmode000_options):
                        cb = QtWidgets.QCheckBox(opt_label)
                        cb.setToolTip(opt_tip)
                        if i < len(default_values) and default_values[i] == "1":
                            cb.setChecked(True)
                        vbox.addWidget(cb)
                        checkboxes.append(cb)
                    groupbox.setToolTip(tooltip)
                    tab_inputs[tab_name][section][key] = checkboxes
                    tab_layout.addRow(groupbox)
                elif widget_type == "padsin_group":
                    groupbox = QtWidgets.QGroupBox(label_text)
                    vbox = QtWidgets.QVBoxLayout(groupbox)
                    buttons = []
                    default_values = [x.strip() for x in default.split(",")] if default else ["0"] * 27
                    for i, (desc, tip) in enumerate(padsin000_options):
                        hbox = QtWidgets.QHBoxLayout()
                        label = QtWidgets.QLabel(f"{i}: {desc}")
                        label.setToolTip(tip)
                        btn = GamepadButtonMapButton(i, default_values[i] if i < len(default_values) else "0")
                        btn.setToolTip(tip)
                        hbox.addWidget(label)
                        hbox.addWidget(btn)
                        vbox.addLayout(hbox)
                        buttons.append(btn)
                    groupbox.setToolTip(tooltip)
                    tab_inputs[tab_name][section][key] = buttons
                    tab_layout.addRow(groupbox)
                elif widget_type == "checkbox":
                    checkbox = QtWidgets.QCheckBox()
                    checkbox.setChecked(str(default).lower() in ("1", "true", "yes", "on"))
                    checkbox.setToolTip(tooltip)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    tab_inputs[tab_name][section][key] = checkbox
                    tab_layout.addRow(label, checkbox)
                elif widget_type == "combobox" and valid:
                    combo = QtWidgets.QComboBox()
                    combo.setToolTip(tooltip)
                    for label_val, value in valid.items():
                        combo.addItem(label_val, value)
                        if str(default) == str(value):
                            combo.setCurrentText(label_val)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    tab_inputs[tab_name][section][key] = combo
                    tab_layout.addRow(label, combo)
                elif widget_type == "spinbox":
                    spin = QtWidgets.QSpinBox()
                    spin.setMinimum(-99999)
                    spin.setMaximum(99999)
                    try:
                        spin.setValue(int(default))
                    except Exception:
                        spin.setValue(0)
                    spin.setToolTip(tooltip)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    tab_inputs[tab_name][section][key] = spin
                    tab_layout.addRow(label, spin)
                else:
                    edit = QtWidgets.QLineEdit(default)
                    edit.setToolTip(tooltip)
                    label = QtWidgets.QLabel(label_text)
                    label.setToolTip(tooltip)
                    tab_inputs[tab_name][section][key] = edit
                    tab_layout.addRow(label, edit)

        self.inputs = {}
        for tab in tab_inputs:
            for section in tab_inputs[tab]:
                if section not in self.inputs:
                    self.inputs[section] = {}
                self.inputs[section].update(tab_inputs[tab][section])

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
        XINPUT_BUTTON_MAP = {
            "B": 0,
            "X": 1,
            "Y": 2,
            "A": 3,
            "DPad Right": 4,
            "DPad Left": 5,
            "DPad Up": 6,
            "DPad Down": 7,
            "LB": 8,
            "LT (Left Trigger)": 9,
            "LStick": 10,
            "RB": 11,
            "RT (Right Trigger)": 12,
            "RStick": 13,
            "Start": 14,
            "Back": 15,
            "None": 16,
            "-1": 16,
            "Left Stick Right": 32,
            "Left Stick Left": 32,
            "Left Stick Up": 33,
            "Left Stick Down": 33,
            "Right Stick Right": 35,
            "Right Stick Left": 35,
            "Right Stick Up": 36,
            "Right Stick Down": 36,
        }

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

        # Detect XInput enabled once, outside the per-key loop
        padmode_widgets = self.inputs.get("padmode000", {}).get("padmode000")
        xinput_enabled = False
        if padmode_widgets and isinstance(padmode_widgets, list) and len(padmode_widgets) > 0:
            xinput_enabled = padmode_widgets[0].isChecked()

        for section, keys in self.ini_structure.items():
            config[section] = {}
            for key, default in keys.items():
                meta = ui_metadata.get(section, {}).get(key, {"widget": "lineedit", "show": True, "tab": section})
                if not meta.get("show", True):
                    continue

                widget = self.inputs.get(section, {}).get(key)
                widget_type = meta.get("widget", "lineedit")

                if widget is None:
                    continue  # Shouldn't happen, but safety first

                if widget_type == "padmode_group":
                    values = ["1" if cb.isChecked() else "0" for cb in widget]
                    config[section][key] = "-1" if all(v == "0" for v in values) else ",".join(values)
                elif widget_type == "padsin_group":
                    if xinput_enabled:
                        # Map button names to XInput values
                        values = []
                        for btn in widget:
                            btn_name = btn.text()
                            mapped_val = XINPUT_BUTTON_MAP.get(btn_name, -1)
                            values.append(str(mapped_val))
                        config[section][key] = "-1" if all(v == "0" for v in values) else ",".join(values)
                    else:
                        # Fallback: just use the button text or value
                        values = [btn.text() for btn in widget]
                        config[section][key] = "-1" if all(v == "0" for v in values) else ",".join(values)
                elif widget_type == "checkbox":
                    config[section][key] = "1" if widget.isChecked() else "0"
                elif widget_type == "combobox":
                    if isinstance(widget, QtWidgets.QComboBox):
                        config[section][key] = widget.currentData()
                    else:
                        config[section][key] = widget.text()
                elif widget_type == "spinbox":
                    config[section][key] = str(widget.value())
                else:  # lineedit and fallback
                    config[section][key] = widget.text()

            # Add hidden keys with their default values
            for key, default in keys.items():
                meta = ui_metadata.get(section, {}).get(key, {"widget": "lineedit", "show": True, "tab": section})
                if not meta.get("show", True) and key not in config[section]:
                    config[section][key] = default

        try:
            with open(ini_path, "w") as f:
                config.write(f)
            QtWidgets.QMessageBox.information(self, "INI Created", f"Created: {ini_path}")
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create INI:\n{e}")
