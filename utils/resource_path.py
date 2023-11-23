import os
import sys


class ResourcePath:
    def __init__(self):
        self.__dirPath = 'resource'

    def setDirPath(self, dirPath: str):
        self.__dirPath = dirPath

    def fileName(self, fileName: str):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        #try:
        #    # PyInstaller creates a temp folder and stores path in _MEIPASS
        #    base_path = sys._MEIPASS
        #except Exception:  
        #    base_path = os.path.abspath("./resource")
        # exe_path = os.path.dirname( os.path.realpath( __file__ ) )

        # return os.path.join(exe_path, self.__dirPath, fileName)

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS # type: ignore
        except Exception:
            base_path = os.path.abspath(self.__dirPath)

        return os.path.join(base_path, fileName)
        