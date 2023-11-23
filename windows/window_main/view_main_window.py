from PyQt5 import QtGui, QtWidgets

from widgets.label_data import LabelData
from widgets.table_view import TableView


class ViewMainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # instansiate
        self.buttons = _ViewMainButtons()
        self.labels = _ViewMainLabels()
        self.mainTable = TableView()
        self.mainTable.verticalHeader().setVisible(False)

        logo = QtWidgets.QLabel('placeholder img')
        
        # Layout
        main = QtWidgets.QHBoxLayout()
        leftBox = QtWidgets.QVBoxLayout()
        leftBoxTop = QtWidgets.QVBoxLayout()
        leftBoxTopSub = QtWidgets.QHBoxLayout()
        rightBox = QtWidgets.QVBoxLayout()
        rightBoxBottom = QtWidgets.QHBoxLayout()
        self.setLayout(main)

        rightBoxBottom.addWidget(self.labels.textMessage)
        rightBoxBottom.addStretch(20)
        rightBoxBottom.addWidget(self.buttons.deleteButton, 10)
        rightBoxBottom.addWidget(self.buttons.saveButton, 10)

        rightBox.addWidget(self.labels.titleData)
        rightBox.addWidget(self.mainTable)
        rightBox.addLayout(rightBoxBottom)

        leftBoxTopSub.addWidget(self.labels.titleMonitor)
        leftBoxTopSub.addStretch()
        leftBoxTopSub.addWidget(self.buttons.startButton)
        leftBoxTopSub.addWidget(self.buttons.stopButton)
        leftBoxTopSub.addWidget(self.buttons.checkButton)

        leftBoxTop.addWidget(self.labels.titleDate)
        leftBoxTop.addWidget(self.labels.displayClock)
        leftBoxTop.addSpacing(20)
        leftBoxTop.addLayout(leftBoxTopSub)
        leftBoxTop.addWidget(self.labels.displayData)

        leftBox.addLayout(leftBoxTop, 75)
        leftBox.addWidget(logo, 25)

        main.addLayout(leftBox, 45)
        main.addLayout(rightBox, 55)

class _ViewMainButtons:
    def __init__(self):
        super().__init__()

        self.startButton = QtWidgets.QPushButton('Start')
        self.stopButton = QtWidgets.QPushButton('Stop')
        self.checkButton = QtWidgets.QPushButton('Check') 
        self.deleteButton = QtWidgets.QPushButton('Delete data')
        self.saveButton = QtWidgets.QPushButton('Save to file')
        self.calculateGrossButton = QtWidgets.QPushButton('Bruto')
        self.calculateTareButton = QtWidgets.QPushButton('Tara')

        self.startButton.setToolTip('Start Monitoring')
        self.stopButton.setToolTip('Stop Monitoring')
        self.checkButton.setToolTip('Check Port')
        self.saveButton.setToolTip('Save Table to File')
        self.calculateGrossButton.setToolTip('Isi Bruto')
        self.calculateTareButton.setToolTip('Hitung Netto')

        self.stopButton.setEnabled(False)


class _ViewMainLabels:
    def __init__(self):
        super().__init__()

        self.titleMonitor = QtWidgets.QLabel('Output Monitor:')
        self.titleData = QtWidgets.QLabel('Data Table:')
        self.titleDate = QtWidgets.QLabel('Date:')
        self.displayClock = QtWidgets.QLabel()
        self.displayClock.setFont(QtGui.QFont('', 25))
        self.displayData = LabelData()
        self.textMessage = QtWidgets.QLabel('Tempelkan kartu untuk menimbang')
        # self.textMessage.setFont(QtGui.QFont('Segoe UI', 8))