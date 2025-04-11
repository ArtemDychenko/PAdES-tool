import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QApplication,
)


class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(" ")
        self.setMinimumWidth(200)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        stylesheet_path = os.path.join(base_dir, "styles.qss")

        with open(stylesheet_path, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.message = QLabel("Write private key password")

        self.input = QLineEdit()
        self.input.setClearButtonEnabled(True)
        self.input.setEchoMode(QLineEdit.EchoMode.Password)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.input)
        layout.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def get_password(self):
        return self.input.text()
