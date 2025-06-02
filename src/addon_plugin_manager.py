import os
import re
from qtpy import QtWidgets
from qtpy import QtWidgets, QtCore
from plugin_descriptions import PLUGIN_DESCRIPTIONS
from allowed_lists import allowed_list

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


class AddonPluginManagerWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Addon & Plugin Manager")
        self.resize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Server selection dropdown (inline with label)
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Server Filter:"))
        self.server_dropdown = QtWidgets.QComboBox()
        self.server_dropdown.addItem("Show All")
        self.server_dropdown.addItems(sorted(allowed_list.keys()))
        self.server_dropdown.currentIndexChanged.connect(self.refresh_tables)
        filter_layout.addWidget(self.server_dropdown)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Tabs for Addons and Plugins
        self.tabs = QtWidgets.QTabWidget()
        self.addons_tab = QtWidgets.QWidget()
        self.plugins_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.addons_tab, "Addons")
        self.tabs.addTab(self.plugins_tab, "Plugins")

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
        
    def refresh_tables(self):
        self.populate_addon_table()
        self.populate_plugin_table()

    def populate_addon_table(self):
        # Clear table
        self.addon_table.setRowCount(0)
        # Look for folders in the addons/ directory
        addons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","Ashita-v4beta-main", "addons")
        addons_dir = os.path.abspath(addons_dir)

        # Get allowed set for selected server
        server = self.server_dropdown.currentText()
        allowed = None
        if server != "Show All":
            allowed = {name.lower() for name in allowed_list.get(server, set())}

        rows = []
        if os.path.isdir(addons_dir):
            for name in sorted(os.listdir(addons_dir)):
                if allowed is not None and name.lower() not in allowed:
                    continue
                full_path = os.path.join(addons_dir, name)
                if os.path.isdir(full_path):
                    lua_path = os.path.join(full_path, f"{name}.lua")
                    desc = extract_addon_description(lua_path)
                    rows.append((name, desc))
        self.addon_table.setRowCount(len(rows))
        for row_idx, (name, desc) in enumerate(rows):
            checkbox_widget = QtWidgets.QWidget()
            checkbox = QtWidgets.QCheckBox()
            if name.lower() in PRECHECKED_ADDONS:
                checkbox.setChecked(True)
            checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
            checkbox_layout.addStretch()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addStretch()
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.addon_table.setCellWidget(row_idx, 0, checkbox_widget)
            name_item = QtWidgets.QTableWidgetItem(name)
            self.addon_table.setItem(row_idx, 1, name_item)
            desc_item = QtWidgets.QTableWidgetItem(desc)
            self.addon_table.setItem(row_idx, 2, desc_item)
        self.addon_table.resizeColumnToContents(0)
        self.addon_table.setColumnWidth(0, min(self.addon_table.columnWidth(0), 32))
        self.addon_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

    def populate_plugin_table(self):
        # Clear table
        self.plugin_table.setRowCount(0)
        plugins_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Ashita-v4beta-main", "plugins")
        plugins_dir = os.path.abspath(plugins_dir)

        # Get allowed set for selected server
        server = self.server_dropdown.currentText()
        allowed = None
        if server != "Show All":
            allowed = {name.lower() for name in allowed_list.get(server, set())}

        rows = []
        if os.path.isdir(plugins_dir):
            for fname in sorted(os.listdir(plugins_dir)):
                if fname.lower().endswith(".dll"):
                    plugin_name = os.path.splitext(fname)[0]
                    if allowed is not None and plugin_name.lower() not in allowed:
                        continue
                    desc = PLUGIN_DESCRIPTIONS.get(plugin_name, "")
                    rows.append((plugin_name, desc))
        self.plugin_table.setRowCount(len(rows))
        for row_idx, (name, desc) in enumerate(rows):
            checkbox_widget = QtWidgets.QWidget()
            checkbox = QtWidgets.QCheckBox()
            if name.lower() in PRECHECKED_PLUGINS:
                checkbox.setChecked(True)
            checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
            checkbox_layout.addStretch()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addStretch()
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.plugin_table.setCellWidget(row_idx, 0, checkbox_widget)
            name_item = QtWidgets.QTableWidgetItem(name)
            self.plugin_table.setItem(row_idx, 1, name_item)
            desc_item = QtWidgets.QTableWidgetItem(desc)
            self.plugin_table.setItem(row_idx, 2, desc_item)
        self.plugin_table.resizeColumnToContents(0)
        self.plugin_table.setColumnWidth(0, min(self.plugin_table.columnWidth(0), 32))
        self.plugin_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)