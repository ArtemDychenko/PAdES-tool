import os
import sys
from typing import Optional

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.uic import loadUi

from pendrive_detection import PenDriveFinder


class MainIU(QMainWindow):
    def __init__(self):
        super(MainIU, self).__init__()
        self.detector = PenDriveFinder()
        ui_path = os.path.join(os.path.dirname(__file__), "design.ui")
        loadUi(ui_path, self)

        # implementation of buttons
        self.sign_button.clicked.connect(self.sign_click_handler)
        self.verification_button.clicked.connect(self.verify_click_handler)

        # implementation of actions in menu
        self.action_choose_pdf_file.triggered.connect(
            self.action_choose_pdf_file_handler
        )
        self.action_exit.triggered.connect(self.close)
        self.action_choose_public_key.triggered.connect(
            self.action_choose_public_key_handler
        )

        # implementation of pendrive detection
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.find_private_key_path)
        self.timer.start(3000)

    def sign_click_handler(self) -> None:
        self.add_log("PDF has been signed")

    def verify_click_handler(self) -> None:
        self.add_log("PDF has been verified")

    def add_log(self, message: str) -> None:
        self.text_browser.append(message)
        cursor = self.text_browser.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_browser.setTextCursor(cursor)
        self.text_browser.ensureCursorVisible()

    def action_choose_pdf_file_handler(self) -> None:
        self.add_log(self.choose_file("PDF files(*.pdf)"))

    def action_choose_public_key_handler(self) -> None:
        self.add_log(self.choose_file("Public key files(*.pem)"))

    def find_private_key_path(self) -> None:
        pen_drives = self.detector.find_all_pen_drives()

        if pen_drives != None:
            self.add_log("Pendrive has been detected")
            for pen_drive in pen_drives:
                self.add_log(pen_drive)
            pen_drive = self.detector.find_pen_drive_with_private_key(pen_drives)

            if pen_drive == None:
                self.add_log("Private key has not been found")

            if pen_drive != None:
                self.add_log("Private key has been found")
                print(self.detector.get_private_key_path(pen_drive))

        else:
            self.add_log("Pendrive has not been detected")


def choose_file(self, name_filter: str) -> Optional[str]:
    file_dialog = QFileDialog(self)
    file_dialog.setWindowTitle("Choose File")
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
    file_dialog.setNameFilter(name_filter)

    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        return selected_files[0]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainIU()
    ui.show()

    # example of status bar
    ui.add_log("Uruchomiono aplikację...")

    app.exec()
