from PyQt5 import QtCore, QtWidgets

from widgets.table_view import TableView


class AdminWin(QtWidgets.QWidget):
    def __init__(self, viewParent):
        super().__init__(viewParent)
        self.setWindowTitle("Truck Administration")
        self.setMinimumWidth(800)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.adminTable = TableView()
        # self.viewtruck.verticalHeader().setVisible(False)

        #Button
        self.addButton = QtWidgets.QPushButton('Add truck')
        self.delButton = QtWidgets.QPushButton('Delete truck')
        self.saveButton = QtWidgets.QPushButton('Save truck list')
        self.msg = QtWidgets.QLabel('Tempelkan kartu rfid jika ingin melakukan registrasi')

        #Layout
        main = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        self.setLayout(main)

        #hlayout.addWidget(self.addbutton)
        hbox.addWidget(self.delButton)
        hbox.addStretch()
        hbox.addWidget(self.msg)

        main.addWidget(self.adminTable)
        main.addLayout(hbox)