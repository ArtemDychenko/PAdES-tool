from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QGridLayout


class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Password")
        self.setFixedSize(300, 70)

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.message = QLabel("Write private key password")

        self.input = QLineEdit()
        self.input.setClearButtonEnabled(True)
        self.input.setEchoMode(QLineEdit.EchoMode.Password)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        layout = QGridLayout()
        layout.addWidget(self.message, 0, 0, 1, 2)
        layout.addWidget(self.input, 1, 0, 1, 1)
        layout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.setLayout(layout)

    def get_password(self):
        return self.input.text()
