import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QLabel, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDesktopServices
from pyzbar.pyzbar import decode
from PIL import Image
import time


class DragAndDropWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_leave_count = 0
        self.setWindowTitle("Drag and Drop QR code scanner")
        self.setGeometry(100, 100, 400, 400)

        self.label = QLabel("Drop QR code image here", self)
        self.label.setGeometry(10, 10, 380, 380)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #999; font-size: 18px;")

        self.setAcceptDrops(True)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            if self.drag_leave_count <= 5:
                self.label.setText("Release to drop")
                self.drag_leave_count += 1
            else:
                self.label.setText("Tashlaysanmi yo'qmi?")

    def dragLeaveEvent(self, event):
        self.label.setText("Drop files here")

    def dropEvent(self, event: QDropEvent):
        self.label.setText("Proccessing...")
        for url in event.mimeData().urls():
            self.dragLeaveEvent(event)
            file_path = url.toLocalFile()
            # print("Dropped file:", file_path)
            result = self.decode_qr(file_path)
            if "success" in result.keys():
                self.label.setText(result["success"])
            else:
                self.label.setText(result["error"])
                time.sleep(2)
                # self.dragLeaveEvent(event)
            self.drag_leave_count = 0

    def mousePressEvent(self, event):
        text = self.label.text()
        if self.label.text().startswith("http://") or \
           self.label.text().startswith("https://"):
            confirmation = QMessageBox.question(
                self,
                "Open URL", f"Do you want to open the URL:\n\n{text}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(QUrl(text))
        else:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.label.text())
            QMessageBox.information(
                self,
                "Text Copied",
                "Text copied to clipboard.")

    def decode_qr(self, img_path):
        try:
            result = decode(Image.open(img_path))

            if result:
                return {"success": result[0].data.decode("utf-8")}
            else:
                return {"error": "Failed to scan"}
        except Exception as e:
            return {"error": str(e)}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragAndDropWindow()
    window.show()
    sys.exit(app.exec())
