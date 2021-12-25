import csv, sys
from PyQt5 import  (QtWinExtras, 
                    QtWidgets, 
                    QtGui, 
                    QtCore, 
                    QtSql)
from module import (MainWin, 
                    TruckAdmin, 
                    ClientWin, 
                    WorkerHelper, 
                    SerialRead, 
                    Image, 
                    res_path)

try:
    # Include in try/except block if you're also targeting Mac/Linux
    myappid = 'mycompany.myproduct.subproduct.version'
    QtWinExtras.QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setWindowTitle("Scale Monitor")
        self._call = WorkerHelper()
        self._client = ClientWin(self)
        self._truck = TruckAdmin(self)
        self._main = MainWin()
        self.id = ''
        self.gross = ''

        # Action Group
        openAction = QtWidgets.QAction('&Open Client Window', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Client Window')
        openAction.triggered.connect(self.openCall)

        saveAction = QtWidgets.QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save data to file')
        saveAction.triggered.connect(self.saveCall)

        exitAction = QtWidgets.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        regAction = QtWidgets.QAction('&Truck Administration', self)
        regAction.setShortcut('Ctrl+T')
        regAction.setStatusTip('Edit truck list')
        regAction.triggered.connect(self.truckCall)

        clearAction = QtWidgets.QAction('&Clear Data', self)
        clearAction.setStatusTip('Clear displayed data')
        clearAction.triggered.connect(self.clear)

        self.unitsAction = QtWidgets.QAction('&Add "Kg" Units', self, checkable=True)
        self.unitsAction.setStatusTip('Add "Kg" units in displayed data')

        # Menubar
        # Create menu bar and add action
        menuBar = self.menuBar()
        rateMenu = QtWidgets.QMenu('&Rate', self)
        self.portMenu = QtWidgets.QMenu('&Ports', self)

        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(regAction)
        fileMenu.addAction(exitAction)

        fileMenu = menuBar.addMenu('&Settings')
        rateGroup = QtWidgets.QActionGroup(rateMenu)
        fileMenu.addMenu(rateMenu)
        rateGroup.setExclusive(True)
        rateGroup.triggered.connect(self._call.chooseRate)
        for rate in self._call.listRate():
            rateAct = QtWidgets.QAction(rate, rateMenu, checkable=True)
            rateMenu.addAction(rateAct)
            rateGroup.addAction(rateAct)
        
        self.portGroup = QtWidgets.QActionGroup(self.portMenu)
        fileMenu.addMenu(self.portMenu)
        self.portGroup.setExclusive(True)
        self.portGroup.triggered.connect(self._call.choosePort)

        PortNone = QtWidgets.QAction('No Serial Port Connected', self, checkable=False)
        self.portMenu.addAction(PortNone)
        self.portGroup.addAction(PortNone)

        fileMenu.addSeparator()
        fileMenu.addAction(clearAction)
        fileMenu.addAction(self.unitsAction)

        #QSignal
        self._call.stat_msg.connect(self.msgbar)

        #Main Win
        self.logo = Image(res_path('logo_new.png'))
        self._main.startbutton.clicked.connect(self.startCall)
        self._main.stopbutton.clicked.connect(self.stopCall)
        self._main.checkbutton.clicked.connect(self.checkCall)
        self._main.delbutton.clicked.connect(self.rowdel)
        self._main.gross.clicked.connect(self.rowadd)
        self._main.tare.clicked.connect(self.rowupdate)
        self._main.savebutton.clicked.connect(self.saveCall)
        self._truck.addbutton.clicked.connect(self.truckadd)
        self._truck.delbutton.clicked.connect(self.truckdel)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_port)
        self.timer.timeout.connect(self.rfidscan)
        self.timer.start(1000)
    
        # Layout
        self.centralWidget = QtWidgets.QWidget()        
        self.setCentralWidget(self.centralWidget)
        self.setStatusBar(self._main.statusBar)

        self.main_layout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()
        self.leftTop = QtWidgets.QVBoxLayout()
        self.leftTopSub = QtWidgets.QHBoxLayout()
        self.rightBottom = QtWidgets.QHBoxLayout()

        self.rightBottom.addWidget(self._main.gross)
        self.rightBottom.addWidget(self._main.tare)
        self.rightBottom.addWidget(self._main.delbutton)
        self.rightBottom.addWidget(self._main.savebutton)
        
        self.right_layout.addWidget(self._main.labeldat)
        self.right_layout.addWidget(self._main.viewtimbang)
        self.right_layout.addLayout(self.rightBottom)

        self.leftTopSub.addWidget(self._main.labelmon)
        self.leftTopSub.addStretch()
        self.leftTopSub.addWidget(self._main.startbutton)
        self.leftTopSub.addWidget(self._main.stopbutton)
        self.leftTopSub.addWidget(self._main.checkbutton)

        self.leftTop.addWidget(self._main.labeldate)
        self.leftTop.addWidget(self._main.label_clock)
        self.leftTop.addSpacing(20)
        self.leftTop.addLayout(self.leftTopSub)
        self.leftTop.addWidget(self._main.label_data)

        self.left_layout.addLayout(self.leftTop)
        #self.left_layout.addSpacing(2)
        self.left_layout.addWidget(self.logo)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)


    def openCall(self):
        if self._client.isVisible():
            pass
        else:
            self._client.show()

    def truckCall(self):
        if self._truck.isVisible():
            pass
        else:
            self._truck.show()

    def exitCall(self):
        sys.exit()

    def startCall(self):
        try:
            self._call.check()
            self._main.stopbutton.setEnabled(True)
            self._main.startbutton.setEnabled(False)
            self.thread = SerialRead()
            self.thread.daemon = True
            self.thread.start()
            self.thread.data_ready.connect(self.dataOutput)
            self.thread.ser_error.connect(self.msgbar)
            
        except:
            self._main.statusBar.showMessage('Set port & rate first', 5000)
            if self._client.isVisible():
                self._client.label_data.setText('Set port & rate first')

    def stopCall(self):
        try:
            self.thread.terminate()
            self.thread.join()
            self._main.stopbutton.setEnabled(False)
            self._main.startbutton.setEnabled(True)
        except:
            pass

    def checkCall(self):
        try:
            self._call.check()
        except:
            self._main.statusBar.showMessage('Port &/rate not selected', 5000)
        
    def msgbar(self,msg):
        self._main.statusBar.showMessage(msg, 5000)
 
    def dataOutput(self, data):
        data1 = None
        data2 = None
        if type(data) is list:
            try:
                data1 = data[0]
                data2 = data[1]
            except:
                data1 = data[0]
        if self.unitsAction.isChecked() and int:
            data1 = data1, 'Kg'
            data1 = ' '.join(data1)
        else:
            pass
        '''print('raw:', data)
        print('data1: ', data1)
        print('data2: ', data2)'''
        self.data1 = data1
        self.data2 = data2 # make false state when in filter list
        self._client.label_data.setText(data1)
        self._main.label_data.setText(data1)
        
    #row group belum bener
    def rowadd(self): # rowadd to nopol_check to id_check if true back to rowadd
        try:
            dbquery = QtSql.QSqlQuery()
            #id_check = self.id_check() #and id_check != self.id
            if self._main.stopbutton.isEnabled() and self.data1 is not None:
                print('im here')
                #self.id = id_check
                if self.id is not None:
                    dbquery.prepare("INSERT INTO hasil_timbang(nopol, tanggal, bruto)"
                                    "VALUES (?, ?, ?)")
                    list = [self.id, self._main.time , self.data1]
                    for insert in list:
                        dbquery.addBindValue(insert)
                    dbquery.exec()
                    self._main.timbang.select()
                    print(dbquery.executedQuery())
                    self.nopol = '' #self.nopol reset just complicated
                elif self.id is None:
                    self.nopol_check()
                    print('here')
                else:
                    self._main.statusBar.showMessage('Data yang dimasukkan tidak cocok/tidak ada', 5000)
        except:
            self._main.statusBar.showMessage('Start monitoring process first', 5000)

    def rowupdate(self):
        try:
            print('try')
            dbquery = QtSql.QSqlQuery()
            id_check = self.id_check()
            get_gross = self.nopol_timbang()
            print('get_gross=', get_gross)
            if self._main.stopbutton.isEnabled() and get_gross is not None:
                #self.id = id_check
                self.gross = get_gross
                netto = float(self.gross) - float(self.data1)
                #netto = round(netto, 2)
                #command = "UPDATE hasil_timbang SET Tara = ?, Netto = ? WHERE Tara IS NULL AND Nopol IS " + id_check
                dbquery.prepare("UPDATE hasil_timbang SET Tara = ?, Netto = ? WHERE Tara IS NULL AND Nopol = ?")
                dbquery.addBindValue(self.data1)
                dbquery.addBindValue(str(round(netto, 2)))
                dbquery.addBindValue(id_check)
                dbquery.exec()
                self._main.timbang.select()
                print(dbquery.executedQuery())
            else:
                print('else')
        except:
            print('except')
            self._main.statusBar.showMessage('Start monitoring process first', 5000)

    def rowdel(self):
        try:
            rowtimbang = self._main.viewtimbang.currentIndex().row()
            self._main.timbang.removeRow(rowtimbang)
            self._main.timbang.select()
        except:
            self._main.statusBar.showMessage('Select row from table first', 5000)

    def truckadd(self):
        #ask something
        #self.nopol_check
        pass

    def truckdel(self):
        rowtruck = self._truck.viewtruk.currentIndex().row()
        self._truck.truk.removeRow(rowtruck)
        self._truck.truk.select()

    def id_check(self): # check if id is valid then return nopol #self.nopol no reset
        dbquery = QtSql.QSqlQuery()
        column = "id"
        val = self.data2 #id ktp
        if self.data2 is None:
            column = "nopol"
            val = self.nopol #nopol

        #print('val=', val)
        command = """SELECT "id", "nopol" from "trucklist" WHERE """ + column + """ = ?"""
        dbquery.prepare(command)
        dbquery.addBindValue(val)
        dbquery.exec()
        dbquery.next()
        if dbquery.isValid():
            #result = [dbquery.value(0), dbquery.value(1)]
            result = dbquery.value(1) #nopol registered in db
            #print(dbquery.isValid())
            return result # return nopol string
        else:
            return None

    def nopol_timbang(self):
        dbquery = QtSql.QSqlQuery()
        dbquery.prepare("""SELECT Bruto from hasil_timbang WHERE Tara IS NULL AND Nopol = ?""")
        dbquery.addBindValue(self.id)
        print('nop=', self.id)
        dbquery.exec()
        dbquery.next()
        if dbquery.isValid():
            result = dbquery.value(0)
            print(dbquery.isValid())
            return result # return bruto
        else:
            return None

    def nopol_ask(self):
        self.timer.stop()
        print(self.data2)
        dbquery = QtSql.QSqlQuery()
        idd = self.data2
        if idd !=0:
            id = idd
            nopol, dialog = QtWidgets.QInputDialog.getText(self, "Nopol Truk", "Masukkan plat nomor truk dibawah")
            nama, dialog1 = QtWidgets.QInputDialog.getText(self, "Nama Supir", "Masukkan nama supir dibawah")
            if id != 0:
                print("masuk = ", id)
                if dialog and dialog1:
                    dbquery.prepare(
                    """
                    INSERT INTO "trucklist"(id, Nopol, Nama) values(?, ?, ?)
                    """)
                    dbquery.addBindValue(id)
                    dbquery.addBindValue(nopol.upper())
                    dbquery.addBindValue(nama.title())
                    dbquery.exec()
                    self._truck.truk.select()
                    id = None
                    self.timer.start(1000)

    def nopol_askmanual(self):
        dbquery = QtSql.QSqlQuery()
        pass
        
    def nopol_check(self):
        self.nopol, dialog = QtWidgets.QInputDialog.getText(self, "Nopol Truk", "Masukkan plat nomor truk dibawah")
        if dialog:
            print(self.nopol)
            self.rowadd()

    def rfidscan(self): # belum jadi
        try:
            id_check = self.id_check()
            #dbquery = QtSql.QSqlQuery()
            if self._truck.isVisible() and self.data2 is not None and self.data2 != '0':
                print('id truck =', self.id_check())
                if self.id_check() is None:
                    #call popup dialog
                    self.nopol_ask()
                else:
                    pass
            if self._truck.isVisible() is not True and self.data2 is not None and self.data2 != '0':
                #print(self.data2)
                if id_check != self.id:# is True:
                    self.id = id_check
                    if self.nopol_timbang():
                        self.rowupdate()
                    else:
                        self.rowadd()
                else:
                    pass
            else:
                #print('im doing else')
                self.id = None
                #self.gross = None
        except:
            pass

    def saveCall(self):
        try:
            print(self.id)
            filter = "XLS Spreadsheet Files (*.csv)"
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', filter)
            with open(name, 'w') as stream:
                print("saving", name)
                writer = csv.writer(stream, delimiter=";", lineterminator="\n")
                for row in range(self._main.viewtimbang.model().rowCount()):
                    rowdata = []
                    for column in range(self._main.viewtimbang.model().columnCount()):
                        item = self._main.viewtimbang.model().index(row, column).data()
                        if item is not None:
                            rowdata.append(item)
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
        except:
            pass

    def clear(self):
        self._main.label_data.clear()
        self._client.label_data.clear()

    def update_port(self):
        find_ports = self._call.listPort()
        if find_ports != self._call.portlist:
            self._call.portlist = find_ports
            self.portMenu.clear()
            for port in self._call.portlist:
                portAct = QtWidgets.QAction(port, self.portMenu, checkable=True)
                self.portMenu.addAction(portAct)
                self.portGroup.addAction(portAct)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if not WorkerHelper.dbconnect():
        sys.exit(1)
    app.setWindowIcon(QtGui.QIcon(res_path('icon.ico')))
    win = MainWindow()
    win.show()
    sys.exit( app.exec_() )