from PyQt5 import QtWidgets

from widgets.submenu_actions import SubMenuActions


class MainMenubar(QtWidgets.QMenuBar):
    def __init__(self):
        super().__init__()

        fileMenu = self.addMenu('File')
        settingsMenu = self.addMenu('Settings')
        adminMenu = self.addMenu('Tools')

        self.actionsMenu = _ActionsMenu(self)
        self.rateMenu = SubMenuActions('Rate', self)
        self.portMenu = SubMenuActions('Ports', self)
        self.addNullPortToView()

        fileMenu.addAction(self.actionsMenu.saveAction)
        fileMenu.addAction(self.actionsMenu.exitAction)

        settingsMenu.addMenu(self.rateMenu)
        settingsMenu.addMenu(self.portMenu)
        settingsMenu.addSeparator()
        settingsMenu.addAction(self.actionsMenu.clearAction)
        settingsMenu.addAction(self.actionsMenu.unitsAction)

        adminMenu.addAction(self.actionsMenu.clientAction)
        adminMenu.addAction(self.actionsMenu.adminAction)
        adminMenu.addAction(self.actionsMenu.debugAction)

    def addRateToView(self, title):
        self.rateMenu.addOption(title)

    def addPortToView(self, title):
        self.portMenu.addOption(title)

    def clearPortToView(self):
        self.portMenu.clear()
    
    def addNullPortToView(self):
        self.portMenu.addNone()

class _ActionsMenu:
    def __init__(self, parent):
        self.saveAction = QtWidgets.QAction('Save', parent)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save data to sheet file')
        
        self.exitAction = QtWidgets.QAction('Exit', parent)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        
        self.clientAction = QtWidgets.QAction('Open Client Window', parent)
        self.clientAction.setShortcut('Ctrl+O')
        self.clientAction.setStatusTip('Open client window')

        self.adminAction = QtWidgets.QAction('Truck Administration', parent)
        self.adminAction.setShortcut('Ctrl+T')
        self.adminAction.setStatusTip('Edit truck list')
        
        self.debugAction = QtWidgets.QAction('Debug Data', parent)
        self.debugAction.setShortcut('Ctrl+Alt+D')
        self.debugAction.setStatusTip('See all incoming data')
        
        self.clearAction = QtWidgets.QAction('Clear Data', parent)
        self.clearAction.setStatusTip('Clear displayed data')
        
        self.unitsAction = QtWidgets.QAction('&Add "Kg" Units', parent)
        self.unitsAction.setCheckable(True)
        self.unitsAction.setStatusTip('Add "Kg" units in displayed data')