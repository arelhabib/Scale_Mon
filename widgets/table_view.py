from PyQt5 import QtWidgets


class TableView(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()

        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    def setTableModel(self, tableModel):
        self.setModel(tableModel)

    def getRow(self):
        return self.currentIndex().row()
    
    def getColumn(self):
        return self.currentIndex().column()
    