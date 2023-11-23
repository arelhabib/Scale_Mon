from windows.window_admin.view_admin_window import AdminWin



class AdminController:
    def __init__(self, viewParent):
        super().__init__()

        self._view = AdminWin(viewParent)

    def openWindow(self):
        if not self._view.isVisible():
            self._view.show()

    def setTableModel(self, tableModel):
        self._view.adminTable.setModel(tableModel)