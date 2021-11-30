import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from utils import *

if __name__ == '__main__':
    cg = config.GetConfig()
    app = QApplication(sys.argv)
    w = MainWindow.Frame(cg, TitleBar, BtnFrame)
    w.show()
    app.exec_()
    cg.save_cf()
    if cg.dbHelper is not None:
        cg.dbHelper.close()
