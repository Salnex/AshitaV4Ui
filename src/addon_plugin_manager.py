import os
import re
from qtpy import QtWidgets
from qtpy import QtWidgets, QtGui
from qtpy.QtCore import Qt
from plugin_descriptions import PLUGIN_DESCRIPTIONS
from allowed_lists import allowed_list
from config import ASHITA_ROOT, PROJECT_ROOT, ASHITA_ADDONS_DIR, ASHITA_PLUGINS_DIR, ASHITA_SCRIPTS_DIR, ASHITA_BOOT_CONFIG_DIR
from download_manager import DownloadManagerWindow

PRECHECKED_ADDONS = {"distance", "fps", "move", "timestamp", "tparty"}
PRECHECKED_PLUGINS = {"thirdparty", "addons", "screenshot","tparty"}

def extract_addon_description(lua_path):
    """Extracts the addon.desc value from a Lua file, if present."""
    try:
        with open(lua_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r'\s*addon\.desc\s*=\s*["\'](.+?)["\']', line)
                if match:
                    return match.group(1)
    except Exception:
        pass
    return None

def qt_keyseq_to_ashita(keyseq_str):
    # Replace Qt modifiers with Ashita symbols
    # Order: Ctrl, Alt, Shift
    out = keyseq_str
    out = out.replace("Ctrl+", "^")
    out = out.replace("Alt+", "!")
    out = out.replace("Shift+", "@")
    return out

class KeybindButton(QtWidgets.QPushButton):
    def __init__(self, key_text, parent=None):
        super().__init__(key_text, parent)
        self.listening = False
        self.default_text = key_text

    def start_listening(self):
        self.setText("Press a key...")
        self.listening = True
        self.grabKeyboard()

    def keyPressEvent(self, event):
        if self.listening:
            key = event.key()
            mods = event.modifiers()
            mods = mods.value  # PySide6/QtPy
            # List of modifier keys to ignore as a "real" keypress
            modifier_keys = {
                Qt.Key_Control,
                Qt.Key_Shift,
                Qt.Key_Alt,
                Qt.Key_Meta,
                Qt.Key_Super_L,
                Qt.Key_Super_R,
                Qt.Key_AltGr,
                Qt.Key_CapsLock,
                Qt.Key_NumLock,
                Qt.Key_ScrollLock,
            }
            if key in modifier_keys:
                return  # Wait for a non-modifier key
            key_seq = QtGui.QKeySequence(mods | key)
            print(f"[DEBUG] Setting keybind to: {key_seq.toString()}")
            self.setText(key_seq.toString())
            self.listening = False
            self.releaseKeyboard()
        else:
            print("[DEBUG] Not listening, passing to super().keyPressEvent")
            super().keyPressEvent(event)

class AddonPluginManagerWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Addons, Plugins, and Keybinds Manager")
        self.resize(600, 400)
        self.setup_ui()

    def accept(self):
        self.save_selection_to_file()
        super().accept()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Server selection dropdown and download button (inline with label)
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Server Filter:"))
        self.server_dropdown = QtWidgets.QComboBox()
        self.server_dropdown.addItem("Show All")
        self.server_dropdown.addItems(sorted(allowed_list.keys()))
        self.server_dropdown.currentIndexChanged.connect(self.refresh_tables)
        download_btn = QtWidgets.QPushButton("Download Addons/Plugins")
        download_btn.clicked.connect(self.open_download_manager)       
        filter_layout.addWidget(self.server_dropdown)
        filter_layout.addStretch()
        filter_layout.addWidget(download_btn)
        layout.addLayout(filter_layout)
        # Download button

        
        # Tabs for Addons and Plugins
        self.tabs = QtWidgets.QTabWidget()
        self.addons_tab = QtWidgets.QWidget()
        self.plugins_tab = QtWidgets.QWidget()
        self.keybinds_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.addons_tab, "Addons")
        self.tabs.addTab(self.plugins_tab, "Plugins")
        self.tabs.addTab(self.keybinds_tab, "Keybinds")

        # Set layouts and tables
        self.addon_table = QtWidgets.QTableWidget()
        self.addon_table.setColumnCount(3)
        self.addon_table.setHorizontalHeaderLabels(["✔", "Addon Name", "Description"])
        self.addon_table.horizontalHeader().setStretchLastSection(True)
        self.addon_table.verticalHeader().setVisible(False)
        self.addon_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.addon_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.addon_table.setShowGrid(True)
        addon_layout = QtWidgets.QVBoxLayout(self.addons_tab)
        addon_layout.addWidget(self.addon_table)

        self.plugin_table = QtWidgets.QTableWidget()
        self.plugin_table.setColumnCount(3)
        self.plugin_table.setHorizontalHeaderLabels(["✔", "Plugin Name", "Description"])
        self.plugin_table.horizontalHeader().setStretchLastSection(True)
        self.plugin_table.verticalHeader().setVisible(False)
        self.plugin_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.plugin_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.plugin_table.setShowGrid(True)
        plugin_layout = QtWidgets.QVBoxLayout(self.plugins_tab)
        plugin_layout.addWidget(self.plugin_table)

        layout.addWidget(self.tabs)

        self.setup_keybinds_tab()

        # OK/Cancel buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        self.refresh_tables()
        
    def setup_keybinds_tab(self):
        layout = QtWidgets.QVBoxLayout(self.keybinds_tab)
        add_btn = QtWidgets.QPushButton("Add New Keybind")
        layout.addWidget(add_btn)

        self.keybinds_table = QtWidgets.QTableWidget()
        self.keybinds_table.setColumnCount(2)
        self.keybinds_table.setHorizontalHeaderLabels(["Key", "Command"])
        self.keybinds_table.horizontalHeader().setStretchLastSection(True)
        self.keybinds_table.verticalHeader().setVisible(False)
        self.keybinds_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.keybinds_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.keybinds_table.setShowGrid(True)
        layout.addWidget(self.keybinds_table)

        # Default keybinds
        default_keybinds = [
            ("Insert", "/ashita"),
            ("SYSRQ", "/screenshot hide"),
            ("Ctrl+V", "/paste"),
            ("F11", "/ambient"),
            ("F12", "/fps"),
            ("Ctrl+F1", "/ta <a10>"),
            ("Ctrl+F2", "/ta <a11>"),
            ("Ctrl+F3", "/ta <a12>"),
            ("Ctrl+F4", "/ta <a13>"),
            ("Ctrl+F5", "/ta <a14>"),
            ("Ctrl+F6", "/ta <a15>"),
            ("Alt+F1", "/ta <a20>"),
            ("Alt+F2", "/ta <a21>"),
            ("Alt+F3", "/ta <a22>"),
            ("Alt+F4", "/ta <a23>"),
            ("Alt+F5", "/ta <a24>"),
            ("Alt+F6", "/ta <a25>"),
        ]
        self.keybinds_table.setRowCount(len(default_keybinds))
        for row, (key, cmd) in enumerate(default_keybinds):
            btn = KeybindButton(key)
            btn.clicked.connect(btn.start_listening)
            self.keybinds_table.setCellWidget(row, 0, btn)
            cmd_edit = QtWidgets.QLineEdit(cmd)
            self.keybinds_table.setCellWidget(row, 1, cmd_edit)

        # Add new row when button is clicked
        def add_new_keybind():
            row = self.keybinds_table.rowCount()
            self.keybinds_table.insertRow(row)
            btn = KeybindButton("Unassigned")
            btn.clicked.connect(btn.start_listening)
            self.keybinds_table.setCellWidget(row, 0, btn)
            cmd_edit = QtWidgets.QLineEdit("")
            self.keybinds_table.setCellWidget(row, 1, cmd_edit)

        add_btn.clicked.connect(add_new_keybind)
    
    def refresh_tables(self):
        self.populate_addon_table()
        self.populate_plugin_table()

    def populate_table(self, table, items_dir, allowed, prechecked_set, desc_lookup_func):
        # Clear table
        table.setRowCount(0)
        rows = []
        if os.path.isdir(items_dir):
            for name in sorted(os.listdir(items_dir)):
                item_path = os.path.join(items_dir, name)
                # Only directories for addons, only .dll files for plugins
                if desc_lookup_func == extract_addon_description:
                    if not os.path.isdir(item_path):
                        continue
                    item_name = name
                else:
                    if not (os.path.isfile(item_path) and name.lower().endswith(".dll")):
                        continue
                    item_name = os.path.splitext(name)[0]
                if allowed is not None and item_name.lower() not in allowed:
                    continue
                desc = desc_lookup_func(os.path.join(item_path, f"{item_name}.lua") if desc_lookup_func == extract_addon_description else item_name)
                rows.append((item_name, desc))
        table.setRowCount(len(rows))
        for row_idx, (name, desc) in enumerate(rows):
            checkbox_widget = QtWidgets.QWidget()
            checkbox = QtWidgets.QCheckBox()
            if name.lower() in prechecked_set:
                checkbox.setChecked(True)
            checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
            checkbox_layout.addStretch()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addStretch()
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row_idx, 0, checkbox_widget)
            name_item = QtWidgets.QTableWidgetItem(name)
            table.setItem(row_idx, 1, name_item)
            desc_item = QtWidgets.QTableWidgetItem(desc)
            table.setItem(row_idx, 2, desc_item)
        table.resizeColumnToContents(0)
        table.setColumnWidth(0, min(table.columnWidth(0), 32))
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

    def populate_addon_table(self):
        # Get allowed set for selected server
        server = self.server_dropdown.currentText()
        allowed = None
        if server != "Show All":
            allowed = {name.lower() for name in allowed_list.get(server, set())}
        self.populate_table(
            self.addon_table,
            ASHITA_ADDONS_DIR,
            allowed,
            PRECHECKED_ADDONS,
            extract_addon_description
        )

    def populate_plugin_table(self):
        # Get allowed set for selected server
        server = self.server_dropdown.currentText()
        allowed = None
        if server != "Show All":
            allowed = {name.lower() for name in allowed_list.get(server, set())}
        self.populate_table(
            self.plugin_table,
            ASHITA_PLUGINS_DIR,
            allowed,
            PRECHECKED_PLUGINS,
            lambda name: PLUGIN_DESCRIPTIONS.get(name, "")
        )

    def save_selection_to_file(self):
        # Get Ashita root
        os.makedirs(ASHITA_SCRIPTS_DIR, exist_ok=True)
        out_path = os.path.join(ASHITA_SCRIPTS_DIR, "addons_plugins.txt")
    
        # Gather checked plugins
        plugin_names = []
        if hasattr(self, "plugin_table"):
            for row in range(self.plugin_table.rowCount()):
                widget = self.plugin_table.cellWidget(row, 0)
                if widget:
                    checkbox = widget.findChild(QtWidgets.QCheckBox)
                    if checkbox and checkbox.isChecked():
                        name_item = self.plugin_table.item(row, 1)
                        if name_item:
                            plugin_names.append(name_item.text())
    
        # Gather checked addons
        addon_names = []
        if hasattr(self, "addon_table"):
            for row in range(self.addon_table.rowCount()):
                widget = self.addon_table.cellWidget(row, 0)
                if widget:
                    checkbox = widget.findChild(QtWidgets.QCheckBox)
                    if checkbox and checkbox.isChecked():
                        name_item = self.addon_table.item(row, 1)
                        if name_item:
                            addon_names.append(name_item.text())
        # Gather keybind commands
        keybind_commands = []
        if hasattr(self, "keybinds_table"):
            for row in range(self.keybinds_table.rowCount()):
                btn = self.keybinds_table.cellWidget(row, 0)
                cmd_edit = self.keybinds_table.cellWidget(row, 1)
                if btn and cmd_edit:
                    key_text = btn.text()
                    command = cmd_edit.text().strip()
                    if key_text and command:
                        ashita_key = qt_keyseq_to_ashita(key_text)
                        keybind_commands.append(f"{ashita_key} {command}")
    
        # Write to file
        with open(out_path, "w", encoding="utf-8") as f:
            for plugin in plugin_names:
                f.write(f"/load {plugin}\n")
            f.write("\n")
            for addon in addon_names:
                f.write(f"/addon load {addon}\n")
            for keybind in keybind_commands:
                f.write(f"/bind {keybind}\n")
        print(f"[DEBUG] Saved selection to {out_path}")
    def open_download_manager(self):
        # Import here to avoid circular import if needed
        dlg = DownloadManagerWindow(self)
        dlg.exec_()