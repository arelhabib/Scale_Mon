from windows.window_client.view_client_window import ClientWin
from utils.data_model import DataModel


class ClientController:
    def __init__(self, viewParent):
        super().__init__()

        self._view = ClientWin(viewParent)
        self.__dataModel = DataModel()


    def updateUI(self):
        self.__setWeightMonitor(self.__dataModel.weight)

    def openWindow(self):
        if not self._view.isVisible():
            self._view.show()

    def __setWeightMonitor(self, data):
        self._view.displayData.setText(data)