from PyQt5 import QtWidgets


class SubMenuActions(QtWidgets.QMenu):
    def __init__(self, title, parent):
        super().__init__(parent)
        self.setTitle(title)
        self.actionGroup = QtWidgets.QActionGroup(self)

    def addOption(self, optionTitle):
        action = self.actionGroup.addAction(optionTitle)
        action.setCheckable(True)
        self.addAction(action)

    def addNone(self):
        action = self.actionGroup.addAction(f'No {self.title()} Are Available')
        action.setCheckable(False)
        self.addAction(action)