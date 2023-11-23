from PyQt5 import QtCore, QtWidgets


class ChildWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(self, parent)
        self.setMinimumWidth(800)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)