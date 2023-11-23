from PyQt5 import QtCore, QtGui, QtWidgets


class Image(QtWidgets.QLabel):
    def __init__(self, img):
        super().__init__()
        
        self.setFrameStyle(QtWidgets.QFrame.Shape.StyledPanel)
        self._pixmap = QtGui.QPixmap(img)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding, 
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

    def paintEvent(self, event):
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self._pixmap.scaled(
            size, 
            QtCore.Qt.AspectRatioMode.KeepAspectRatio, 
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        point.setX(int((size.width() - scaledPix.width())/2))
        point.setY(int((size.height() - scaledPix.height())/2))
        painter.drawPixmap(point, scaledPix)