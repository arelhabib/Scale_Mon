import time

from PyQt5 import QtCore

from db.db_controller import DBController
from utils.config_model import ConfigModel
from utils.data_model import DataModel
from utils.signal_manager import SignalManager
from widgets.dialog_collections import inputDialog
from windows.window_mode import WindowMode
from worker.serial_thread import SerialThread


class WorkerController:
    def __init__(self, signal: 'SignalManager', dbCon: 'DBController'):
        super().__init__()

        self.__config = ConfigModel()
        self.__dataModel = DataModel()
        self.__query = dbCon
        self.__signalManager = signal
        # self.__windowController = windowController

        self.__autoTimer = QtCore.QTimer()
        self.__autoTimer.timeout.connect(self.__rfidScan)
        # self.otherTimer = QtCore.QTimer()
        # self.otherTimer.start(500)
        # self.otherTimer.timeout.connect(self.checkAutoTimer)
        
        self.__monitorMode = None
        self.__NopolID = None

    def startWorker(self):
        self.checkConfig()

        self.monitorThread = SerialThread(self.__signalManager, self.__config.getConfig())
        self.monitorThread.daemon = True
        self.monitorThread.start()

        # NOTE: the "if statement" result faster than the thread exception
        time.sleep(0.1) # hehe
        if not self.monitorThread._running:
            raise
        
        self.__config.toggleRunner()
        self.__startAutoTimer()

    def stopWorker(self):
        self.monitorThread.terminate()
        self.monitorThread.join()
        self.__config.toggleRunner()
        self.__stopAutoTimer()

    def checkConfig(self):
        try:
            port = self.__config.getConfig()['port']
            rate = self.__config.getConfig()['rate']

            self.__signalManager.sendStatusBarPayload(f'Port {port} with rate {rate} b/s selected')
        except:
            self.__signalManager.sendStatusBarPayload('Port &/rate not selected')

    def setMonitorMode(self, monitorMode):
        self.__monitorMode = monitorMode
        if self.__config.isThreadActive:
            self.__checkTimerDebugWin()

    def checkAutoTimer(self):
        print(self.__autoTimer.isActive())

    # TODO: create toggle input read by monitor if started
    def toggleAutoInput(self):
        self.__config.toggleAutoInput()

    def __startAutoTimer(self):
        self.__autoTimer.start(1000)

    def __stopAutoTimer(self):
        self.__autoTimer.stop()

    def __checkTimerDebugWin(self):
        if self.__monitorMode == WindowMode.DEBUG:
            if self.__autoTimer.isActive():
                self.__stopAutoTimer()
        else:
            if not self.__autoTimer.isActive() and self.__monitorMode != WindowMode.ADMIN:
                self.__startAutoTimer()

    def __rfidScan(self):
        """isi data otomatis berdasarkan data RFID yang didapat"""

        # TODO: test the thing
        rfid = self.__dataModel.rfid
        nopolResult = self.__query.findNopolbyRFID(rfid)

       
        if self.__monitorMode == WindowMode.MAIN:
            if nopolResult:
                if nopolResult != self.__NopolID:
                    self.__NopolID = nopolResult
                    brutoResult = self.__query.findBrutobyNopol(self.__NopolID)
                    
                    if brutoResult:
                        self.__query.mainAddTareAndCalculateNetto(self.__dataModel.weight, brutoResult, self.__NopolID)
                    else:
                        time = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, HH:mm:ss")
                        self.__query.mainAddGross(nopolResult, time, self.__dataModel.weight)

            if not rfid:
                self.__NopolID = None
        
        if self.__monitorMode == WindowMode.ADMIN:
            if not nopolResult and rfid:
                self.__stopAutoTimer()

                if rfid != 0:
                    # NOTE: why do i need to use rfidPassCheck?
                    rfidPassCheck = rfid
                    nopol, dialogNopol = inputDialog("Nopol Truk", "Masukkan plat nomor truk dibawah")
                    nama, dialogNama = inputDialog("Nama Supir", "Masukkan nama supir dibawah")
                    if rfidPassCheck != 0:
                        if dialogNopol and dialogNama:
                            self.__query.adminRegisTruck(rfidPassCheck, nama, nopol)
                            
                            print('basically success')
                            self.__startAutoTimer()
                        else:
                            print('you came here')
                            self.__startAutoTimer()

        # else:
        #     print('reset')
        #     self.__NopolID = None

       