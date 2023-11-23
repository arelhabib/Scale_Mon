from PyQt5 import QtSql


class DBQuery(QtSql.QSqlQuery):
    def initDB(self):
        self.exec(
            """
            CREATE TABLE "hasil_timbang" (
            "Nopol"	    TEXT NOT NULL,
            "Tanggal"	TEXT NOT NULL,
            "Bruto"	    INTEGER,
            "Tara"	    INTEGER,
            "Netto"	    INTEGER
            )
            """
        )
        self.exec(
            """
            CREATE TABLE "trucklist"(
            "id"	TEXT PRIMARY KEY,
            "Nopol"	TEXT,
            "Nama"  TEXT
            )
            """
        )

    def addGross(self, rfidData, timestamp, weightData):
        self.prepare(
            """
            INSERT INTO hasil_timbang(nopol, tanggal, bruto) VALUES (?, ?, ?)
            """
        )
        self.addBindValue(rfidData)
        self.addBindValue(timestamp)
        self.addBindValue(weightData)
        self.exec()

    def addTareAndCalculateNetto(self, weightData, grossWeight, nopol):
        netto = float(grossWeight) - float(weightData)
        
        self.prepare(
            """
            UPDATE hasil_timbang SET Tara = ?, Netto = ? WHERE Tara IS NULL AND Nopol = ?
            """
        )
        self.addBindValue(weightData)
        self.addBindValue(str(round(netto, 2)))
        self.addBindValue(nopol)
        self.exec()
    
    def addNewTruck(self, rfidData, nama, nopol):
        self.prepare(
            """
            INSERT INTO "trucklist"(id, Nopol, Nama) VALUES(?, ?, ?)
            """
        )
        self.addBindValue(rfidData)
        self.addBindValue(nopol.upper())
        self.addBindValue(nama.title())
        self.exec()

    def findGrossByNopol(self, nopol):
        self.prepare(
            """
            SELECT Bruto from hasil_timbang WHERE Tara IS NULL AND Nopol = ?
            """
        )
        self.addBindValue(nopol)
        self.exec()
        self.next()
        if self.isValid():
            gross = self.value(0)
            return gross
        else:
            return None
        
    def checkRFIDThenReturnNopol(self, rfidData, column= "id" ):
        self.prepare(
            """
            SELECT "id", "nopol" from "trucklist" WHERE """ + column + """ = ?
            """
        )
        self.addBindValue(rfidData)
        self.exec()
        self.next()
        if self.isValid():
            nopol = self.value(1)
            return nopol
        else:
            return None