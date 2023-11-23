from PyQt5 import QtCore, QtWidgets

from windows.window_main.view_main_menubar import MainMenubar
from windows.window_main.view_main_window import ViewMainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.viewUI = ViewMainWindow()
        self.viewUIMenu = MainMenubar()

        self.setCentralWidget(self.viewUI)
        self.setMenuBar(self.viewUIMenu)
        self.setMinimumSize(QtCore.QSize(800,500))
        self.setWindowTitle('Scale Monitor')
        self.statusBar().setStyleSheet('padding-left:8px;color:black;font-weight:bold;')
        self.show()

    def showToStatusBar(self, msg):
        self.statusBar().showMessage(msg, 5000)