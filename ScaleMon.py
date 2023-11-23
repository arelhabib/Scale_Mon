import sys

from PyQt5 import QtWidgets, QtGui

from app_controller import AppController
from utils.resource_path import ResourcePath

try:
    # Include in try/except block if you're also targeting Mac/Linux
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    icon = ResourcePath().fileName('icon.ico')
    app.setWindowIcon(QtGui.QIcon(icon))

    mainApp = AppController()

    sys.exit(app.exec_())