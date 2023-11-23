from PyQt5 import QtCore, QtWidgets

from widgets.label_data import LabelData


class DebugWin(QtWidgets.QWidget):
    def __init__(self, viewParent):
        super().__init__(viewParent)
        self.setWindowTitle("Debug Data Window")
        self.setFixedWidth(350)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        rawTitle = QtWidgets.QLabel("Raw Data")
        weighTitle = QtWidgets.QLabel("Weight Data:")
        rfidTitle = QtWidgets.QLabel("RFID Data:")
        self.displayRaw = _LabelDebug()
        self.displayWeight = _LabelDebug()
        self.displayRfid = _LabelDebug()

        main = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2= QtWidgets.QHBoxLayout()
        hbox3= QtWidgets.QHBoxLayout()
        self.setLayout(main)

        hbox1.addWidget(rawTitle, 25)
        hbox1.addWidget(self.displayRaw, 75)
        hbox2.addWidget(weighTitle, 25)
        hbox2.addWidget(self.displayWeight, 75)
        hbox3.addWidget(rfidTitle, 25)
        hbox3.addWidget(self.displayRfid, 75)
        main.addLayout(hbox1)
        main.addLayout(hbox2)
        main.addLayout(hbox3)

class _LabelDebug(LabelData):
    def __init__(self):
        super().__init__()

        self.multiplier = 0.05
        self.setMinimumHeight(30)
