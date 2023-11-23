from PyQt5 import QtCore, QtSql


# NOTE: row/column flags
# QtCore.Qt.ItemIsEnabled
# QtCore.Qt.ItemIsSelectable
# QtCore.Qt.ItemIsEditable
class QSqlTableTimbang(QtSql.QSqlTableModel):
    def __init__(self):
        super().__init__()
        self.setTable('hasil_timbang')
        self.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()

    def flags(self, index):
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable

class QSqlTableTruck(QtSql.QSqlTableModel):
    def __init__(self):
        super().__init__()
        self.setTable('trucklist')
        self.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()

    def flags(self, index):
        if(index.column() == 0):
            return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
        else:    
            return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable