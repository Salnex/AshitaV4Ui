import os
from qtpy import QtWidgets

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