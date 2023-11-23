from PyQt5 import QtCore, QtGui, QtWidgets


class Image(QtWidgets.QLabel):
    def __init__(self, img):
        super().__init__()
        
        self.setFrameStyle(QtWidgets.QFrame.Shape.StyledPanel)
        self.pixmap = QtGui.QPixmap(img)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding, 
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

    def paintEvent(self, event):
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self.pixmap.scaled(
            size, 
            QtCore.Qt.AspectRatioMode.KeepAspectRatio, 
            transformMode = QtCore.Qt.TransformationMode.SmoothTransformation
        )
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)
        painter.drawPixmap(point, scaledPix)