from PyQt5 import QtCore
from serial.tools import list_ports


class MainModel:
    def __init__(self):
        self.portlist = []

    def listRate(self):
        r = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
        return r
    
    def listPort(self):
        ports = list_ports.comports()
        port = []   
        for p in ports:
            port.append(p.device)
        return port
    
    def getTime(self):
        time = QtCore.QDateTime.currentDateTime().toString("dd-MM-yyyy, HH:mm:ss")
        return time