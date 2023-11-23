from typing import Callable
from PyQt5 import QtCore


# NOTE: cant use it as singleton
class SignalManager(QtCore.QObject):
    _instance = None
    __payloadStatusbar = QtCore.pyqtSignal(str)
    __payloadRawData = QtCore.pyqtSignal(object)

    def sendStatusBarPayload(self, data: str):
        self.__payloadStatusbar.emit(data)
    
    def receiveStatusBarPayload(self, func: Callable):
        self.__payloadStatusbar.connect(func)

    def sendRawDataPayload(self, data: object):
        self.__payloadRawData.emit(data)

    def receiveRawDataPayload(self, func: Callable):
        self.__payloadRawData.connect(func)