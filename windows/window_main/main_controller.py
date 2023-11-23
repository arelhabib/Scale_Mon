import csv
import sys

from PyQt5 import QtCore

from utils.config_model import ConfigModel
from utils.data_model import DataModel
from utils.signal_manager import SignalManager
from widgets.dialog_collections import saveDialog
from windows.window_main.main_model import MainModel
from windows.window_main.main_window import MainWindow


class MainController:
    def __init__(self, signal: 'SignalManager'):
        super().__init__()
        
        self._view = MainWindow()
        self.__model = MainModel()

        self.__config = ConfigModel()
        self.__dataModel = DataModel()
        self.__signal = signal

        self.actionControl = self._view.viewUIMenu.actionsMenu
        self.buttonControl  = self._view.viewUI.buttons
        self.menuBarControl = self._view.viewUIMenu

        self.__initController()

        

    def __initController(self):
        # signal
        self.__signal.receiveStatusBarPayload(self.__updateStatusbar)

        # actionMenu
        self.actionControl.exitAction.triggered.connect(lambda: sys.exit())
        self.actionControl.saveAction.triggered.connect(self.saveToFile)
        self.actionControl.clearAction.triggered.connect(self.__clearOutput)

        # menuBar
        self.menuBarControl.rateMenu.actionGroup.triggered.connect(self.__chooseRate)
        self.menuBarControl.portMenu.actionGroup.triggered.connect(self.__choosePort)
        self.__loadRate()

        self.buttonControl.saveButton.clicked.connect(self.saveToFile)

    def updateUI(self):
        self.__updateTime()
        self.__loadPorts()
        self.__updateOutputMonitor(self.__dataModel.weight)

    def __clearOutput(self):
        self._view.viewUI.labels.displayData.clear()

    def __addUnitsOutput(self):
        pass

    def __choosePort(self, action):
        self.__config.setPort(action.text())

    def __chooseRate(self, action):
        self.__config.setRate(action.text())

    def __updateTime(self):
        self._view.viewUI.labels.displayClock.setText(self.__model.getTime())

    def __updateStatusbar(self, msg):
        self._view.showToStatusBar(msg)

    def __updateOutputMonitor(self, weightData):
        self._view.viewUI.labels.displayData.setText(weightData)

    def __loadRate(self):
        for item in self.__model.listRate():
            self.menuBarControl.addRateToView(item)

    def __loadPorts(self):
        listPortResult = self.__model.listPort()
        if listPortResult != self.__model.portlist:
            self.__model.portlist = listPortResult
            self.menuBarControl.clearPortToView()

            if len(self.__model.portlist) < 1:
                self.menuBarControl.addNullPortToView()
            else:
                for port in self.__model.portlist:
                    self.menuBarControl.addPortToView(port)

    def saveToFile(self):
        """save to .csv"""
        docPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation(1)) #DocumentLocation
        fileFilter = "CSV (Comma Separated Values) (*.csv)"
        name, fileType = saveDialog('Save File', docPath, fileFilter)
        
        if fileType:
            with open(name, 'w') as stream:
                print("saving", name)
                writer = csv.writer(stream, delimiter=";", lineterminator="\n")
                for row in range(self._view.viewUI.mainTable.model().rowCount()):
                    rowdata = []
                    for column in range(self._view.viewUI.mainTable.model().columnCount()):
                        item = self._view.viewUI.mainTable.model().index(row, column).data()
                        if item is not None:
                            rowdata.append(item)
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

    def setTableModel(self, tableModel):
        self._view.viewUI.mainTable.setModel(tableModel)

    def startMonitor(self):
        self.buttonControl.startButton.setEnabled(False)
        self.buttonControl.stopButton.setEnabled(True)
        
    def stopMonitor(self):
        self.buttonControl.startButton.setEnabled(True)
        self.buttonControl.stopButton.setEnabled(False)
        
    