from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication, QTreeView
from PyQt6.QtGui import QTextCursor, QFileSystemModel
from PyQt6.QtCore import QSortFilterProxyModel, Qt

import os
import sys

class MainIU(QMainWindow):
    def __init__(self):
        super(MainIU, self).__init__()
        loadUi("design.ui", self)

        ## implementation of files view
        self.model = QFileSystemModel()
        self.model.setRootPath("/")

        self.treeView.setModel(self.model)

        home_directory = os.path.expanduser("~")
        self.treeView.setRootIndex(self.model.index(home_directory))

        ## implementation of buttons
        self.signButton.clicked.connect(self.sign_click_handler)
        self.verificationButton.clicked.connect(self.verify_click_handler)



    def sign_click_handler(self):
        self.add_log("PDF has been signed")

    def verify_click_handler(self):
        self.add_log("PDF has been verified")

    def add_log(self, message):
        self.textBrowser.append(message)

        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainIU()
    ui.show()

    ## example of status bar
    ui.add_log("Uruchomiono aplikację...")
    ui.add_log("Start detecting pendrive...")
    ui.add_log("Pendrive detected!")

    app.exec()




