from typing import Any


class ConfigModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.isAutoInput = True
        self.isThreadActive = False
        self.__config: dict[str, Any] = {}
        self.__initConfig()

    def __initConfig(self):
        self.__config = {
            'timeout': 3, # 1 or None
            'parity': 'N',
            'stopbits': 1,
            # 'port': None,
            # 'rate': None
            }
        
    def getConfig(self):
        return self.__config
    
    def setDefault(self):
        self.__initConfig()

    def toggleRunner(self):
        self.isThreadActive = not self.isThreadActive

    def toggleAutoInput(self):
        self.isAutoInput = not self.isAutoInput
    
    def setPort(self, port):
        self.__config['port'] = port

    def setRate(self, rate):
        self.__config['rate'] = rate
    
