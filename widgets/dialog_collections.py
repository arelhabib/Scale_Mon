from PyQt5 import QtWidgets


def showDbErrorMessage(err: str):
    QtWidgets.QMessageBox.critical(
        None,
        "Error!",
        f"Database Error: {err}",
    )

def inputDialog(title: str, description: str):
    return QtWidgets.QInputDialog.getText(
        None, 
        title, 
        description
    )

def saveDialog(title: str, docPath: str, fileType: str):
    return QtWidgets.QFileDialog.getSaveFileName(
        None, 
        title, 
        docPath, 
        fileType
    )
