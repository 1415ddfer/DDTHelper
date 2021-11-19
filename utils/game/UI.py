import os
import time

import win32gui
import win32process

from PyQt5 import QtWidgets, QAxContainer, QtGui
from PyQt5.QtCore import QProcess, QUrl, pyqtSignal
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

from utils.game.default import *


class GameUI(QtWidgets.QMainWindow):
    web = 0
    flash_con = 0
    has_out_tis = 0

    def __init__(self, title, icon):
        super(GameUI, self).__init__()
        self.p = QProcess(self)
        self.has_out_tis = False

        self.resize(1000, 623)
        self.m_title = title
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout0 = QtWidgets.QHBoxLayout(main_widget)
        self.layout0.setSpacing(0)
        self.layout0.setContentsMargins(0, 0, 0, 0)  # 布局无边框
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon))

        self.menu_bar = self.menuBar()
        self.init_menu()

    login_signal = pyqtSignal(int)

    def init_menu(self):
        m_setting = self.menu_bar.addMenu('设置菜单')

        set_pic = QtWidgets.QMenu('画质调整', self)
        pic_group = QtWidgets.QActionGroup(self)
        pic_high = QtWidgets.QAction('高画质', self)
        pic_high.setCheckable(True)
        pic_low = QtWidgets.QAction('低画质', self)
        pic_low.setCheckable(True)
        pic_high.triggered.connect(lambda: self.flashEvent(0))
        pic_low.triggered.connect(lambda: self.flashEvent(1))
        pic_group.addAction(pic_high)
        pic_group.addAction(pic_low)
        set_pic.addAction(pic_high)
        set_pic.addAction(pic_low)
        pic_high.setChecked(True)

        self.menu_bar.addMenu(m_setting)

        m_setting.addMenu(set_pic)

        m_audio = QtWidgets.QAction('关闭声音', self)
        m_setting.addAction(m_audio)

        m_pr = QtWidgets.QAction('开启防触', self)
        m_pr.triggered.connect(lambda: self.has_out_tis)
        m_setting.addAction(m_pr)

        m_resize = QtWidgets.QAction('恢复正常大小', self)
        m_resize.triggered.connect(lambda: self.resize(1000, 623))
        m_setting.addAction(m_resize)

        self.m_plugin = QtWidgets.QMenu('插件', self)
        self.m_plugin.setIcon(QtGui.QIcon(TITLE_PLUGIN_STOPPED))
        self.menu_bar.addMenu(self.m_plugin)

        m_reload = QtWidgets.QAction('重新登陆', self)
        m_reload.triggered.connect(lambda: self.login_signal.emit(1))
        self.menu_bar.addAction(m_reload)

        m_about = QtWidgets.QAction('关于..', self)
        self.menu_bar.addAction(m_about)

    def init_web(self, acc):
        self.web = _Browser(acc)
        self.layout0.addWidget(self.web)

    def init_flash(self, s, url):
        if self.web:
            self.layout0.removeWidget(self.web)
            self.web.clear_all()
            self.web.deleteLater()
        if s:
            self.p.start('plugin\\flashplayer_sa.exe', [url])
            self.p.waitForFinished(1000)
            subPid = self.p.processId()
            print(subPid)
            while True:
                time.sleep(0.2)
                hwnd = self.pid2hwnd(str(subPid), 'ShockwaveFlash', 'flashplayer_sa')
                if hwnd:
                    break
            window = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
            window.resize(1000, 600)
            self.layout0.addWidget(window)
        else:
            self.flash_con = QAxContainer.QAxWidget()
            self.layout0.addWidget(self.flash_con)
            self.flash_con.setControl(
                "{D27CDB6E-AE6D-11CF-96B8-444553540000}")  # flash的com接口，ShockwaveFlash.ShockwaveFlash.34
            self.flash_con.dynamicCall("SetWMode(string)", "direct")
            self.flash_con.dynamicCall("LoadMovie(long,string)", 0, url)

    @staticmethod
    def startSA(url):
        str0 = "(start-process -FilePath flashplayer_sa.exe -ArgumentList " + url + " -PassThru).id"
        return os.popen(str0).read()

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
        print(res)
        for i in res.split('\n'):
            if i is not None and i != '':
                if a:
                    a = int(i.split('=')[1])
                    break
                if i == 'ProcessId=' + p:
                    a = 1
        print(a)
        if a == 1:
            a = int(p)
        print(a)
        for i in hwnd_list:
            if win32process.GetWindowThreadProcessId(i)[1] == a:
                return i

    def update_state(self, text):
        self.setWindowTitle(self.m_title + '   |   ' + text)

    def flashEvent(self, e):
        if self.flash_con:
            match e:
                case 0:
                    self.flash.dynamicCall("SetQuality2(string)", "high")
                case 1:
                    self.flash.dynamicCall("SetQuality2(string)", "low")

    def change_tis(self):
        self.has_out_tis = not self.has_out_tis

    def closeEvent(self, e):
        if self.has_out_tis:
            result = QMessageBox.information(self, "退出提醒",
                                             "你确定要退出游戏?",
                                             QMessageBox.Yes |
                                             QMessageBox.No)
            if result == QMessageBox.Yes:
                print("执行退出动作")
                self.close()


class _Browser(QWebEngineView):
    isLogin = 0
    js_res = None
    url = None
    Sid = None

    def __init__(self, acc):
        super(_Browser, self).__init__()
        self.acc = acc
        self.setFixedSize(1000, 600)
        match acc[0]:
            case 1:
                self.load(QUrl(SERVER_4399(acc[1])))
            case 2:
                self.load(QUrl(SERVER_7K7K(acc[1])))
        self.loadFinished.connect(self.get_web_state)

    url_signal = pyqtSignal(int, str)

    def get_web_state(self):
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
                self.url_signal.emit(1, GAME_4399(self.Sid, res))
            case 2:
                self.get_url_43()
                self.isLogin += 1
            case 1:
                self.Sid = res.split('&')[4].split('=')[1]
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
                                self.stop_alert()
                                self.isLogin = 1
                                self.get_iframe_43()
                    case 'web.7k7k.com':
                        pass

                    case _:
                        if res.split('/')[3]:
                            print('网址错误或游戏运营商暂未收录')

    def login_in_7k(self):
        print('执行登陆')
        js = '''document.getElementById('username').setRangeText("''' + self.acc[3] + '''");\
        document.querySelector('#password').setRangeText("''' + self.acc[4] + '''");\
        document.querySelector("#loginbtn").click() '''
        self.page().runJavaScript(js)

    def login_in_43(self):
        js = '''
        function DDTHelper()
        {   
            try {
                document.getElementById('s_user').setRangeText("''' + self.acc[3] + '''");\
                document.querySelector('#s_password').setRangeText("''' + self.acc[4] + '''");\
                document.querySelector("body > div > div.main.login_main > div > table > tbody > tr > td > dl > dd > div.loginbox > form > ul:nth-child(2) > li:nth-child(2) > input").click() 
            }catch(err) {
                res0 = err.message;
            }
        }
        
        DDTHelper();
        '''
        self.page().runJavaScript(js)

    def get_iframe_43(self):
        js = '''        
        function DDTHelper()
        {
            try {
                res0 = window.frames["game_box"].getAttribute('src');
            }catch(err) {
                res0 = err.message;
            }
            return res0;
        }

        DDTHelper();
        '''
        self.page().runJavaScript(js, self.call_back)

    def get_url_43(self):
        js = '''        
        function DDTHelper()
        {
            try {
                res0 = document.evaluate('/html/body/table/tbody/tr/td/table/tbody/tr/td/object/embed',document).iterateNext().getAttribute('src');
            }catch(err) {
                res0 = err.message;
            }
            return res0
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