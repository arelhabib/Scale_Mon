from PyQt5 import QtCore

from db.db_controller import DBController
from utils.data_model import DataModel
from utils.signal_manager import SignalManager
from windows.window_admin.admin_controller import AdminController
from windows.window_client.client_controller import ClientController
from windows.window_debug.debug_controller import DebugController
from windows.window_main.main_controller import MainController
from windows.window_mode import WindowMode
from worker.worker_controller import WorkerController


class AppController:
    def __init__(self):
        super().__init__()

        self.dbController = DBController()
        self.dataModel = DataModel()
        self.signalManager = SignalManager()
        self.workerController = WorkerController(self.signalManager, self.dbController)

        # window
        self.main = MainController(self.signalManager)
        self.client = ClientController(self.main._view)
        self.admin = AdminController(self.main._view)
        self.debug = DebugController(self.main._view)

        self.timer = QtCore.QTimer()
        self.timer.start(50)
        self.timer.timeout.connect(self.updateAllUI)
        self.timer.timeout.connect(self.setWindowMode)

        self.windowMode = WindowMode.MAIN
        self.signalManager.receiveRawDataPayload(self.updateDataModel)

        self.crossInitialization()

    def crossInitialization(self):
        # main
        self.main.actionControl.clientAction.triggered.connect(self.client.openWindow)
        self.main.actionControl.adminAction.triggered.connect(self.openAdminWindow)
        self.main.actionControl.debugAction.triggered.connect(self.openDebugWindow)

        self.main.buttonControl.checkButton.clicked.connect(self.workerController.checkConfig)
        self.main.buttonControl.startButton.clicked.connect(self.startMonitor)
        self.main.buttonControl.stopButton.clicked.connect(self.stopMonitor)

        
        # table view & model
        self.main.setTableModel(self.dbController.mainTableModel)
        self.admin.setTableModel(self.dbController.adminTableModel)

        self.main.buttonControl.deleteButton.clicked.connect(self.deleteItemMainTable)
        self.admin._view.delButton.clicked.connect(self.deleteItemAdminTable)

    def updateAllUI(self):
        self.main.updateUI()
        self.client.updateUI()
        self.debug.updateUI()

    def openAdminWindow(self):
        if not self.debug._view.isVisible():
            self.admin.openWindow()
        else:
            self.signalManager.sendStatusBarPayload('Close Debug Window first')

    def openDebugWindow(self):
        if not self.admin._view.isVisible():
            self.debug.openWindow()
        else:
            self.signalManager.sendStatusBarPayload('Close Admin Window first')

    def startMonitor(self):
        try:
            self.workerController.startWorker()
            self.main.startMonitor()
        except:
            pass

    def stopMonitor(self):
        try:
            self.workerController.stopWorker()
            self.main.stopMonitor()
        except:
            pass

    def updateDataModel(self, rawData):
        dataSplit = rawData.split(', ')
        weightData = ''
        rfidData = ''

        if type(dataSplit) is list:
            weightData = dataSplit[0]
            try:
                if dataSplit[1] != '0':
                    rfidData = dataSplit[1]
            except:
                pass

        self.dataModel.updateRawData(rawData)
        self.dataModel.updateWeight(weightData)
        self.dataModel.updateRFID(rfidData)

    def setWindowMode(self):
        admin = self.admin._view.isVisible()
        debug = self.debug._view.isVisible()
        
        if admin:
            self.windowMode = WindowMode.ADMIN
        elif debug:
            self.windowMode = WindowMode.DEBUG
        else:
            self.windowMode = WindowMode.MAIN

        self.workerController.setMonitorMode(self.windowMode)

    def deleteItemMainTable(self):
        row = self.main._view.viewUI.mainTable.getRow()
        self.dbController.mainDeleteRow(row)

    def deleteItemAdminTable(self):
        row = self.admin._view.adminTable.getRow()
        self.dbController.adminDeleteTruckRow(row)

    