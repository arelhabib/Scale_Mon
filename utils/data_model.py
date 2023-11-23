class DataModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.weight  = ''
        self.rfid    = ''
        self.nopol   = ''
        self.rawData = ''

    def updateWeight(self, weight: str):
        self.weight = weight
        
    def updateRFID(self, rfid: str):
        self.rfid = rfid
    
    def updateNopol(self, nopol: str):
        self.nopol = nopol

    def updateRawData(self, rawData: str):
        self.rawData = rawData