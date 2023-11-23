from utils.data_model import DataModel
from windows.window_debug.view_debug_window import DebugWin


class DebugController:
    def __init__(self, viewParent):
        super().__init__()

        self._view = DebugWin(viewParent)
        self.__dataModel = DataModel()

    def openWindow(self):
        if not self._view.isVisible():
            self._view.show()

    def updateUI(self):
        self.__setRawData(self.__dataModel.rawData)
        self.__setRFIDData(self.__dataModel.rfid)
        self.__setWeightData(self.__dataModel.weight)

    def __setRawData(self, data):
        self._view.displayRaw.setText(data)
    
    def __setRFIDData(self, data):
        self._view.displayRfid.setText(data)

    def __setWeightData(self, data):
        self._view.displayWeight.setText(data)

