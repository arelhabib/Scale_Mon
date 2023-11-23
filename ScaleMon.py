import sys

from PyQt5 import QtWidgets

from app_controller import AppController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    mainApp = AppController()

    sys.exit(app.exec_())