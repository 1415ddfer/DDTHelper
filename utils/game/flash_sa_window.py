import os
import subprocess
import time

import win32gui
import win32process
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget


class Example(QMainWindow):

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.p = QProcess(self)
        self.initUI()

    def initUI(self):
        # import threading
        # t = threading.Thread(target=self.runExe)
        # t.start()
        self.p.start('plugin\\flashplayer_sa.exe', [self.url], )
        self.p.waitForFinished(1000)
        subPid = self.p.processId()
        print(subPid)
        time.sleep(1)
        while True:
            time.sleep(0.2)
            hwnd = self.pid2hwnd(str(subPid), 'ShockwaveFlash', 'flashplayer_sa')
            if hwnd:
                break

        window = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
        window.resize(1000, 600)
        self.setCentralWidget(window)
        self.setFixedSize(1000, 625)
        self.show()

    @staticmethod
    def pid2hwnd(p, c, t):
        def get_all_hwnd(hwnd, mouse):
            if win32gui.IsWindow(hwnd) \
                    and win32gui.IsWindowEnabled(hwnd) \
                    and win32gui.IsWindowVisible(hwnd) \
                    and win32gui.GetClassName(hwnd) == c:
                hwnd_list.append(hwnd)

        hwnd_list = []
        win32gui.EnumWindows(get_all_hwnd, 0)
        print(hwnd_list)
        if not hwnd_list:
            return 0
        str0 = '''wmic process where (name like '%%''' + t + '''%%')get processid /value'''
        res = os.popen(str0).read()
        a = 0
        for i in res.split('\n'):
            if i is not None and i != '':
                if a:
                    a = int(i.split('=')[1])
                    break
                if i == 'ProcessId=' + p:
                    a = 1
        print(a)
        for i in hwnd_list:
            if win32process.GetWindowThreadProcessId(i)[1] == a:
                return i

    def runExe(self):
        exePath = "plugin\\flashplayer_sa.exe"
        p = subprocess.Popen(exePath)
        self.subPid = p.pid


# MacromediaFlashPlayerActiveX
# ShockwaveFlash
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example('')
#     sys.exit(app.exec_())
