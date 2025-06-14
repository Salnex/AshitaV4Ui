import os
import importlib.util
from qtpy import QtWidgets, QtCore
from allowed_lists import allowed_list
from config import ASHITA_ADDONS_DIR, ASHITA_PLUGINS_DIR, REPOS_DIR, ASHITA_DOWNLOADS_DIR
import requests
import zipfile
import shutil
import tempfile


class DownloadManagerWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Addons/Plugins")
        self.resize(700, 500)
        self.repo_items = self.load_repo_items()
        self.filtered_items = self.repo_items.copy()
        self.setup_ui()
        print(f"Looking for repositories in: {REPOS_DIR}")
        print(f"Loaded {len(self.repo_items)} items from repositories.")

    def load_repo_items(self):
        items = []
        for fname in os.listdir(REPOS_DIR):
            if fname.endswith(".py"):
                print(f"Loading repository file: {fname}")
                path = os.path.join(REPOS_DIR, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], path)
                mod = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(mod)
                    if isinstance(mod.__dict__.get("__builtins__"), dict):
                        # Remove __builtins__ if present (from exec_module)
                        del mod.__dict__["__builtins__"]
                    # Expecting a list at the top level
                    for obj in mod.__dict__.values():
                        if isinstance(obj, list):
                            items.extend(obj)
                except Exception as e:
                    print(f"Failed to load {fname}: {e}")
        return items

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Server filter dropdown
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Server Filter:"))
        self.server_dropdown = QtWidgets.QComboBox()
        self.server_dropdown.addItem("Show All")
        self.server_dropdown.addItems(sorted(allowed_list.keys()))
        self.server_dropdown.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.server_dropdown)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table for repo items
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Name", "Version", "Author", "Description", "Category", "Download"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Close button
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)
        self.populate_table()

    def apply_filters(self):
        server = self.server_dropdown.currentText()
        if server == "Show All":
            self.filtered_items = self.repo_items.copy()
        else:
            allowed = allowed_list.get(server, set())
            self.filtered_items = [
                item for item in self.repo_items
                if item.get("name", "").lower() in allowed
            ]
        # TODO: Add filtering for already downloaded items here
        self.populate_table()

    def populate_table(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for item in self.filtered_items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(item.get("name", "")))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(item.get("version", "")))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(item.get("author", "")))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(item.get("description", "")))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(item.get("category", "")))
            # Placeholder download button
            btn = QtWidgets.QPushButton("Download")
            btn.clicked.connect(lambda _, i=item: self.download_and_install(i))
            self.table.setCellWidget(row, 5, btn)
        self.table.setSortingEnabled(True)

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self, "Download Error", message)

    def download_and_install(self, item):
        url = item.get("link")
        link_type = item.get("link_type", "direct")
        name = item.get("name")
        typ = item.get("type")
        path_to_content = item.get("path_to_content_folder")
        if not url or not name or not typ or not path_to_content:
            self.show_error("Missing required fields in repo entry.")
            return

        if link_type != "direct":
            self.show_error(f"Unsupported link_type: {link_type}")
            return

        # Download zip
        try:
            self.setEnabled(False)
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            local_zip = os.path.join(ASHITA_DOWNLOADS_DIR, f"{name}.zip")
            os.makedirs(ASHITA_DOWNLOADS_DIR, exist_ok=True)
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(local_zip, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except Exception as e:
            self.setEnabled(True)
            QtWidgets.QApplication.restoreOverrideCursor()
            self.show_error(f"Failed to download: {e}")
            return

        # Extract zip
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(local_zip, "r") as zip_ref:
                    zip_ref.extractall(tmpdir)
                # Find the content folder
                content_path = os.path.join(tmpdir, *path_to_content)
                if not os.path.exists(content_path):
                    raise FileNotFoundError(f"Content path not found: {content_path}")

                # Determine destination
                if typ == "plugin":
                    dest_dir = ASHITA_PLUGINS_DIR
                elif typ == "addon":
                    dest_dir = os.path.join(ASHITA_ADDONS_DIR, name)
                else:
                    raise ValueError(f"Unknown type: {typ}")
                print(f"Installing {name} to {dest_dir}")
                os.makedirs(dest_dir, exist_ok=True)

                # Copy all files/folders from content_path to dest_dir
                for item_name in os.listdir(content_path):
                    src = os.path.join(content_path, item_name)
                    dst = os.path.join(dest_dir, item_name)
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
        except Exception as e:
            self.setEnabled(True)
            QtWidgets.QApplication.restoreOverrideCursor()
            self.show_error(f"Failed to extract/copy: {e}")
            return
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
            self.setEnabled(True)

        QtWidgets.QMessageBox.information(self, "Success", f"{name} downloaded and installed!")