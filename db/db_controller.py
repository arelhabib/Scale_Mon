import sys

from PyQt5 import QtSql

from db.db_query import DBQuery
from db.table_model import QSqlTableTimbang, QSqlTableTruck
from widgets.dialog_collections import showDbErrorMessage


class DBController:
    def __init__(self):
        super().__init__()

        self.__dbInstance = QtSql.QSqlDatabase().addDatabase("QSQLITE")
        self.__dbInstance.setDatabaseName('bambang.db')

        if not self.__dbInstance.open():
            showDbErrorMessage(self.__dbInstance.lastError().databaseText())
            sys.exit()

        self.__dbQuery = DBQuery()
        self.__dbQuery.initDB()

        self.adminTableModel = QSqlTableTruck()
        self.mainTableModel = QSqlTableTimbang()

    def findNopolbyRFID(self, rfid):
        return self.__dbQuery.checkRFIDThenReturnNopol(rfid)
    
    # table admin
    def adminDeleteTruckRow(self, index):
        self.adminTableModel.removeRow(index)
        self.adminTableModel.select()

    def adminRegisTruck(self, rfid, nama, nopol):
        self.__dbQuery.addNewTruck(rfid, nama, nopol)
        self.adminTableModel.select()

    # table main
    def findBrutobyNopol(self, nopol):
        return self.__dbQuery.findGrossByNopol(nopol)
    
    def mainDeleteRow(self, index):
        self.mainTableModel.removeRow(index)
        self.mainTableModel.select()

    def mainAddGross(self, nopol, date, weightMonitor):
        self.__dbQuery.addGross(nopol, date, weightMonitor)
        self.mainTableModel.select()

    def mainAddTareAndCalculateNetto(self, weightMonitor, weightGross, nopol):
        self.__dbQuery.addTareAndCalculateNetto(weightMonitor, weightGross, nopol)
        self.mainTableModel.select()