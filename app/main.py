from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication, QTreeView, QFileDialog
from PyQt6.QtGui import QTextCursor, QFileSystemModel
from PyQt6.QtCore import QSortFilterProxyModel, Qt, QDir, QModelIndex

import os
import sys


# class PdfFilterProxyModel(QSortFilterProxyModel):
#     def __init__(self):
#         super().__init__()
#
#     def filterAcceptsRow(self, source_row, source_parent):
#         """
#                 Returns true if the item in the row indicated by the given source_row
#                 and source_parent should be included in the model; otherwise returns false.
#
#                 Parameters:
#                     source_row – int
#                     source_parent – PySide2.QtCore.QModelIndex
#
#                 Returns:
#                     bool: True if the item should be included in the model, False otherwise.
#                 """
#         model = self.sourceModel()
#         index = model.index(source_row, 0, source_parent)
#
#         if model.isDir(index):
#             directory_path = model.filePath(index)
#             return self.contains_pdf(directory_path)
#         else:
#             return model.filePath(index).lower().endswith(".pdf")
#
#     def contains_pdf(self, directory_path):
#         """
#                 Returns true if the directory contains pdf file; otherwise returns false.
#
#                 Parameters:
#                     directory_path -`str`
#
#                 Returns:
#                     bool: True if there is pdf file, False otherwise.
#                 """
#         iterator = QDir(directory_path).entryInfoList(
#             filters=QDir.Filter.Files | QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot,
#             sort=QDir.SortFlag.Name,
#         )
#         for entity in iterator:
#             if entity.isDir():
#                 if self.contains_pdf(entity.filePath()): return True
#             elif entity.suffix().lower() == "pdf":
#                 return True
#         return False


class MainIU(QMainWindow):
    def __init__(self):
        super(MainIU, self).__init__()
        loadUi("design.ui", self)


        ## implementation of buttons
        self.signButton.clicked.connect(self.sign_click_handler)
        self.verificationButton.clicked.connect(self.verify_click_handler)

        ##implementation of actions in menu
        self.actionChoose_file.triggered.connect(self.action_choose_file_handler)
        self.actionexit.triggered.connect(self.close)

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


    def action_choose_file_handler(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.add_log("Selected File:"+selected_files[0])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainIU()
    ui.show()

    ## example of status bar
    ui.add_log("Uruchomiono aplikację...")
    ui.add_log("Start detecting pendrive...")
    ui.add_log("Pendrive detected!")

    app.exec()
