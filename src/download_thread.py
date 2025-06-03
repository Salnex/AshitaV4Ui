from qtpy.QtCore import QThread, Signal
import requests

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