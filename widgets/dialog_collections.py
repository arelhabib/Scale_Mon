from PyQt5 import QtWidgets, QtCore


def showDbErrorMessage(err: str):
    QtWidgets.QMessageBox.critical(
        QtWidgets.QApplication.activeWindow(),
        "Error!",
        f"Database Error: {err}",
    )

def inputDialog(title: str, description: str):
    return QtWidgets.QInputDialog.getText(
        QtWidgets.QApplication.activeWindow(), 
        title, 
        description,
        flags= QtCore.Qt.WindowType.WindowCloseButtonHint
    )

def saveDialog(title: str, docPath: str, fileType: str):
    return QtWidgets.QFileDialog.getSaveFileName(
        None, 
        title, 
        docPath, 
        fileType
    )
