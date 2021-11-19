import os
import subprocess
import sys
import time
from multiprocessing import Process, Value
from threading import Thread
from ctypes import c_char_p

import win32gui
import win32process
from PyQt5.QtCore import QUrl, QProcess, QThread, pyqtSignal
from PyQt5.QtGui import QWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMdiArea


class login(QWebEngineView):
    isLogin = 0
    js_res = None

    get_web_state = '''
        function DDTHelper()
        {
            return window.location.href;
        }

        DDTHelper();
        '''

    def __init__(self, acc, v):
        super(login, self).__init__()
        self.acc = acc
        self.v = v
        self.setFixedSize(1000, 620)
        url = 'http://web.4399.com/stat/togame.php?target=ddt&server_id=S179'
        url7k = 'http://web.7k7k.com/user/login.html?refer=http%3A%2F%2Fweb.7k7k.com%2Fgames%2Ftogame.php%3Ftarget%3Dddt_7%26server_id%3D196'
        self.load(QUrl(url))
        self.loadFinished.connect(self.get_web_state0)

    def get_web_state0(self):
        js = '''
        function DDTHelper()
        {
            return window.location.href;
        }

        DDTHelper();
        '''
        self.page().runJavaScript(js, self.call_back)

    def stop_alert(self):
        js = '''
        var WinAlerts = window.alert;
        window.alert = function (e) {
        if (e != null && e.indexOf("提示内容")>-1)
        {
            //和谐了
        }else{
            WinAlerts (e);
        }
        };'''
        self.page().runJavaScript(js)

    def call_back(self, res):
        print('返回为：' + res)
        if res is None:
            return
        match self.isLogin:
            case 3:
                self.v.value = res.encode("utf-8")
            case 2:
                self.get_url_43()
                self.isLogin += 1
            case 1:
                self.load(QUrl(res))
                self.isLogin += 1
            case 0:
                host = res.split('/')[2]
                match host:
                    case 'web.4399.com':
                        state0 = res.split('/')[3]
                        match state0:
                            case 'user':
                                self.login_in_43()
                            case 'stat':
                                print('1')
                                self.stop_alert()
                                self.isLogin = 1
                                try:
                                    self.get_iframe_43()
                                except Exception as e:
                                    print(e)
                    case 'web.7k7k.com':
                        pass

                    case _:
                        if res.split('/')[3]:
                            print('网址错误或游戏运营商暂未收录')

    def login_in_7k(self):
        print('执行登陆')
        js = '''document.getElementById('username').setRangeText("''' + self.acc[0] + '''");\
        document.querySelector('#password').setRangeText("''' + self.acc[1] + '''");\
        document.querySelector("#loginbtn").click() '''
        self.page().runJavaScript(js)

    def login_in_43(self):
        js = '''document.getElementById('s_user').setRangeText("''' + self.acc[0] + '''");\
        document.querySelector('#s_password').setRangeText("''' + self.acc[1] + '''");\
        document.querySelector("body > div > div.main.login_main > div > table > tbody > tr > td > dl > dd > div.loginbox > form > ul:nth-child(2) > li:nth-child(2) > input").click() '''
        self.page().runJavaScript(js)

    def get_iframe_43(self):
        js = '''        
        function DDTHelper()
        {
            return window.frames["game_box"].getAttribute('src');
        }
        
        DDTHelper();
        '''
        self.page().runJavaScript(js, self.call_back)

    def get_url_43(self):
        js = '''        
        function DDTHelper()
        {
            return document.evaluate('/html/body/table/tbody/tr/td/table/tbody/tr/td/object/embed',document).iterateNext().getAttribute('src');
        }

        DDTHelper();
        '''
        self.page().runJavaScript(js, self.call_back)

    def get_url_7k(self):
        js = '''
        function DDTHelper()
        {
            return document.querySelector("#iframepage");
        }
        
        DDTHelper();
        '''
        self.page().runJavaScript(js, self.call_back)

    def get_url_7k_2(self):
        print(self.js_res)

    def clear_all(self):
        self.page().profile().clearAllVisitedLinks()
        self.page().profile().clearHttpCache()
        p_cookie = self.page().profile().cookieStore()
        p_cookie.deleteAllCookies()
        p_cookie.deleteSessionCookies()


class _main(QMainWindow):

    class webThread(QThread):
        def __init__(self, w, t, s):
            super().__init__()
            self.w = w
            self.s = s
            self.t = t

        update_signal = pyqtSignal(int, str)

        def run(self) -> None:
            while True:
                time.sleep(0.2)
                print(self.w.value)
                if int(self.w.value):
                    break
            self.update_signal.emit(self.w.value, None)

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

    def __init__(self, acc):
        super().__init__()
        self.acc = acc
        self.p = QProcess()

        self.setFixedSize(1000, 600)
        self.initThread()

    def update_win(self, hwnd, url) -> None:
        wg = QWidget.createWindowContainer(hwnd)
        wg.resize(1000, 600)
        self.setCentralWidget(wg)
        self.qp.join()
        self.p.start('plugin\\flashplayer_sa.exe "' + url + '"')
        self.p.waitForFinished(2000)
        while True:
            time.sleep(0.2)
            hwnd = self.webThread.pid2hwnd(str(self.p.processId()), 'ShockwaveFlash', 'flashplayer_sa')
            if hwnd:
                break
        window = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
        window.resize(1000, 600)
        self.setCentralWidget(window)
        self.setFixedSize(1000, 625)

    def initThread(self):
        web = Value('i', 0)
        self.v = Value(c_char_p, 'ss'.encode("utf-8"))
        self.qp = Process(target=self.start_browser, args=(self.acc, self.v, web))
        self.qp.start()
        self.t = self.webThread(web, self.qp, self.v)
        self.t.update_signal.connect(self.update_win)
        self.t.start()

    @staticmethod
    def start_browser(acc, v, hwnd):
        app0 = QApplication(sys.argv)

        web = login(acc, v)
        hwnd.value = int(web.winId())
        app0.exec_()


if __name__ == '__main__':
    acc0 = ['b1783488228', '565656']
    app = QApplication(sys.argv)
    win = _main(acc0)
    win.show()
    app.exec_()
