import time

from PyQt5.QtCore import pyqtSignal, QProcess, QThread


class PluginThread(QProcess):
    class ThreadShell(QThread):
        def __init__(self, control=None, args0=None, ojb=None):
            QThread.__init__(self)
            ojb.control = control
            ojb.args = args0
            ojb.state_signal = self.state_signal
            self.ojb = ojb

        state_signal = pyqtSignal(int, str)

        def run(self):
            self.state_signal.emit(1, '正在运行')
            try:
                self.ojb.run()
            except Exception as e:
                print(e)

    def __init__(self, control=None, args0=None, ojb=None, flag=None):
        QProcess.__init__(self)
        self.state0 = True
        self.flag = flag
        self.Thread = self.ThreadShell(control, args0, ojb)
        self.Thread.state_signal.connect(self.up_date)

    state_signal = pyqtSignal(int, str)

    def up_date(self, i0, s0):
        self.state_signal.emit(i0, s0)

    def change_state(self, f):
        self.state0 = f

    def run(self):
        self.state0 = True
        self.flag.connect(self.change_state)
        self.Thread.setDaemon(True)
        self.Thread.start()
        while self.state0:
            if not self.m_thread.is_alive():
                print('线程完毕')
                break
            time.sleep(1)

        self.up_date(0, '脚本已停止运行')
        print('已经退出')
