import threading
from typing import Any

import serial

from utils.signal_manager import SignalManager


# NOTE: threads cannot deals with singleton
class SerialThread(threading.Thread):
    """Get Data from Serial decode to utf-8"""
    def __init__(self, signal: 'SignalManager', config: 'dict[str, Any]'):
        super().__init__()

        self._running = True
        self.__signal = signal
        self.__config = config
        self.__serial = serial.Serial()

        self.__serial.timeout = self.__config['timeout'] 
        self.__serial.parity = self.__config['parity']
        self.__serial.stopbits = self.__config['stopbits']
        # s.bytesize = 8 # if something wrong use this
        self.__serial.port = self.__config['port']
        self.__serial.baudrate = self.__config['rate']
        

    def terminate(self):
        self._running = False
        self.__serial.close()

    def run(self):
        try:
            self.__serial.open()

            while self.__serial.is_open & self._running:
                rawdata = self.__serial.readline()
                try:
                    # strip any endline
                    text = rawdata.rstrip().decode('utf-8')
                except:
                    text = rawdata.hex()
                self.__signal.sendRawDataPayload(text)
                
        except Exception as e:
            self._running = False
            self.__signal.sendStatusBarPayload('Port busy / Disconnected')
            print("err: ", e)