from PyQt5 import QtCore, QtWidgets

from widgets.label_data import LabelData


class ClientWin(QtWidgets.QWidget):
    def __init__(self, viewParent):
        super().__init__(viewParent)
        self.setWindowTitle("Client Window")
        self.setMinimumWidth(800)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.labelTitle = QtWidgets.QLabel("Output:")
        self.labelTitle.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, 
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.labelTitle.setMaximumHeight(40)
        
        self.displayData = LabelData()
        self.displayData.multiplier = 0.19
        self.displayData.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, 
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        main = QtWidgets.QVBoxLayout()
        self.setLayout(main)

        main.addWidget(self.labelTitle)
        main.addWidget(self.displayData)