from qtpy import QtWidgets, QtCore

class qtpyTerminal(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: black; color: pink; font-family: Consolas; font-size: 14px;")
        self.appendPlainText("AI Shell ready...\n")

    def start(self):
        self.appendPlainText("Shell started...\n")

    def stop(self):
        self.appendPlainText("Shell stopped.\n")

