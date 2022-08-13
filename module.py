import sys, os, threading, serial
from serial.tools import list_ports
from PyQt5 import  (QtWidgets, 
                    QtGui, 
                    QtCore, 
                    QtSql)


#Utils
def res_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

def dbconnect():
        con = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("database.db")
        if not con.open():
            QtWidgets.QMessageBox.critical(
                None,
                "Error!",
                "Database Error: %s" % con.lastError().databaseText(),
            )
            return False
        createTableQuery = QtSql.QSqlQuery()
        createTableQuery.exec(
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
        createTableQuery.exec(
            """
            CREATE TABLE "trucklist"(
            "id"	TEXT PRIMARY KEY,
            "Nopol"	TEXT,
            "Nama"  TEXT
            )
            """
        )
        # beware of not null
        return True

class WorkerHelper(QtCore.QObject):
    stat_msg = QtCore.pyqtSignal(object)
    def __init__(self):
        QtCore.QRunnable.__init__(self)
        self.portlist = []
     
    def listPort(self):
        ports = list_ports.comports()
        port = []   
        for p in ports:
            port.append(p.device)
        return port

    def listRate(self):
        r = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
        return r
    
    def choosePort(self, action):
        global port
        port = action.text()
    
    def chooseRate(self, action):
        global rate
        rate = action.text()

    def check(self):
        try:
            txt = port, 'with', rate, 'b/s selected'
            disp = ' '.join(txt)
            self.stat_msg.emit(disp)
        except:
            raise



# RAPIIN LAGI
class SerialRead(threading.Thread, QtCore.QObject):
    """Get Data from Serial decode to utf-8"""
    data_ready = QtCore.pyqtSignal(object)
    ser_error = QtCore.pyqtSignal(object)
    def __init__(self):
        threading.Thread.__init__(self)
        QtCore.QObject.__init__(self)
        self._running = True
        self.ser = serial.Serial()
        self.ser.timeout = 3 # 1 or None
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        #s.bytesize = 8 // if something wrong use this
        self.ser.port = port
        self.ser.baudrate = rate

    def terminate(self):
        self._running = False
        self.ser.close()

    def run(self):
        try:
            self.ser.open()
            #and self.ser.is_open and is True
            while self.ser.is_open and self._running is True:
                rawdata = self.ser.readline()
                try:
                    #text = rawdata.decode('ASCII')
                    text = rawdata.rstrip().decode('utf-8')
                except:
                    text = rawdata.hex()
                self.data_ready.emit(text)
                
        except Exception as e:
            self.ser_error.emit('Port busy / Disconnected')
            print(e)
        

class IPCam():
    def __init__(self):
        pass

class DebugWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Debug Data Window")
        self.setFixedWidth(350)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.Window)
        height      = 30
        multiplier  = 0.05

        self.label = LabelData()
        self.label.setMinimumHeight(30)
        self.label.multiplier = 0.10

        self.label_raw = QtWidgets.QLabel("Raw Data")
        self.label_weight = QtWidgets.QLabel("Weight Data:")
        self.label_rfid = QtWidgets.QLabel("RFID Data:")
        self.raw = LabelData()
        self.weight = LabelData()
        self.rfid = LabelData()
        
        self.raw.setMinimumHeight(height)
        self.raw.multiplier = multiplier
        self.weight.setMinimumHeight(height)
        self.weight.multiplier = multiplier
        self.rfid.setMinimumHeight(height)
        self.rfid.multiplier = multiplier

        main = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        hbox2= QtWidgets.QHBoxLayout()
        hbox3= QtWidgets.QHBoxLayout()
        self.setLayout(main)

        hbox.addWidget(self.label_raw, 25)
        hbox.addWidget(self.raw, 75)
        hbox2.addWidget(self.label_weight, 25)
        hbox2.addWidget(self.weight, 75)
        hbox3.addWidget(self.label_rfid, 25)
        hbox3.addWidget(self.rfid, 75)
        main.addLayout(hbox)
        main.addLayout(hbox2)
        main.addLayout(hbox3)

class ClientWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Client Window")
        self.setMinimumWidth(800)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.Window)

        self.label = QtWidgets.QLabel("Output:")
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.setMaximumHeight(40)
        
        self.label_data = LabelData()
        self.label_data.multiplier = 0.19
        self.label_data.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        main = QtWidgets.QVBoxLayout()
        self.setLayout(main)

        main.addWidget(self.label)
        main.addWidget(self.label_data)

class TruckAdmin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Truck Administration")
        self.setMinimumWidth(800)
        self.setContentsMargins(3,3,3,3)
        self.setWindowFlags(QtCore.Qt.Window)

        #Table model
        self.truk = QSqlTableTruck()
        self.truk.setTable("trucklist")
        self.truk.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.truk.select()

        self.viewtruk = QtWidgets.QTableView()
        self.viewtruk.setModel(self.truk)
        #self.viewtruk.verticalHeader().setVisible(False)
        self.viewtruk.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        #Button
        self.addbutton = QtWidgets.QPushButton('Add truck')
        self.delbutton = QtWidgets.QPushButton('Delete truck')
        self.savebutton = QtWidgets.QPushButton('Save truck list')
        self.msg = QtWidgets.QLabel('Tempelkan kartu rfid jika ingin melakukan registrasi')

        #Layout
        main = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        self.setLayout(main)

        #hlayout.addWidget(self.addbutton)
        hlayout.addWidget(self.delbutton)
        hlayout.addStretch()
        hlayout.addWidget(self.msg)

        main.addWidget(self.viewtruk)
        main.addLayout(hlayout)

class MainWin(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        #Label
        self.labelmon = QtWidgets.QLabel('Output Monitor:')
        self.labeldat = QtWidgets.QLabel('Data Table:')
        self.labeldate = QtWidgets.QLabel('Date:')
        self.label_clock = QtWidgets.QLabel()
        self.label_clock.setFont(QtGui.QFont('', 25))
        self.label_data = LabelData()
        self.msg = QtWidgets.QLabel('Tempelkan kartu untuk menimbang')
        self.msg.setFont(QtGui.QFont('Segoe UI', 8))

        #Statusbar
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setStyleSheet("padding-left:8px;color:black;font-weight:bold;")

        #Button
        self.startbutton = QtWidgets.QPushButton('Start')
        self.stopbutton = QtWidgets.QPushButton('Stop')
        self.checkbutton = QtWidgets.QPushButton('Check') 
        self.delbutton = QtWidgets.QPushButton('Delete data')
        self.gross = QtWidgets.QPushButton('Bruto')
        self.tare = QtWidgets.QPushButton('Tara')
        self.savebutton = QtWidgets.QPushButton('Save to file')

        self.startbutton.setToolTip('Start Monitoring')
        self.stopbutton.setToolTip('Stop Monitoring')
        self.checkbutton.setToolTip('Check Port')
        self.gross.setToolTip('Isi Bruto')
        self.tare.setToolTip('Hitung Netto')
        self.savebutton.setToolTip('Save Table to File')

        #Model View
        self.timbang = QSqlTableTimbang()
        self.timbang.setTable("hasil_timbang")
        self.timbang.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        '''self.timbang.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.timbang.setHeaderData(1, QtCore.Qt.Horizontal, "NoPol")
        self.timbang.setHeaderData(2, QtCore.Qt.Horizontal, "Tanggal")
        self.timbang.setHeaderData(3, QtCore.Qt.Horizontal, "Bruto")
        self.timbang.setHeaderData(4, QtCore.Qt.Horizontal, "Tara")
        self.timbang.setHeaderData(5, QtCore.Qt.Horizontal, "Netto")'''
        self.timbang.select()
      
        #Set the view
        self.viewtimbang = QtWidgets.QTableView()
        self.viewtimbang.setModel(self.timbang)
        self.viewtimbang.verticalHeader().setVisible(False)
        self.viewtimbang.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        #Clock
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showdate)
        timer.start(1)

    def showdate(self):
        self.time = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, HH:mm:ss")
        self.label_clock.setText(self.time)

#Subclassing
class Image(QtWidgets.QLabel):
    def __init__(self, img):
        QtWidgets.QLabel.__init__(self)
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.pixmap = QtGui.QPixmap(img)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

    def paintEvent(self, event):
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation)
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)
        painter.drawPixmap(point, scaledPix)

class LabelData(QtWidgets.QLabel):
    def __init__(self):
        QtWidgets.QLabel.__init__(self)
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet('border: 1px solid darkgray;background-color: white;')
        self.setMinimumHeight(300)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.multiplier = 0.14

    def resizeEvent(self, event):
        font = self.font()
        font.setPixelSize(self.width() * self.multiplier)
        self.setFont(font)

# QtCore.Qt.ItemIsEnabled
# QtCore.Qt.ItemIsSelectable
# QtCore.Qt.ItemIsEditable
class QSqlTableTimbang(QtSql.QSqlTableModel):
    def __init__(self):
        QtSql.QSqlTableModel.__init__(self)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

class QSqlTableTruck(QtSql.QSqlTableModel):
    def __init__(self):
        QtSql.QSqlTableModel.__init__(self)

    def flags(self, index):
        if(index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:    
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable