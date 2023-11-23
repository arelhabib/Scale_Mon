from PyQt5 import QtCore, QtWidgets


class LabelData(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('border: 1px solid darkgray;background-color: white;')
        self.setMinimumHeight(300)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, 
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.multiplier = 0.14

    def resizeEvent(self, event):
        font = self.font()
        font.setPixelSize(int(self.width() * self.multiplier))
        self.setFont(font)