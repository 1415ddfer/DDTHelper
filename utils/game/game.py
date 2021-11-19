import os
import sys
from multiprocessing import Process
from utils.game.gamePlugin import *
from utils.game.login import *

import requests.utils
from PyQt5 import QAxContainer, QtWidgets, QtCore, QtGui
from bs4 import BeautifulSoup
from selenium import webdriver
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume



def save_res(web):
    with open('./userdata/data_tmp.txt', 'a', encoding='utf-8') as f:
        text = str(web)
        f.write(text)


class Ui_Flash(QAxContainer.QAxWidget):
    def __init__(self, url, title):
        super(Ui_Flash, self).__init__()
        self.resize(1000, 600)  # 设置窗口的大小

        self.setControl("{D27CDB6E-AE6D-11CF-96B8-444553540000}")  # flash的com接口，ShockwaveFlash.ShockwaveFlash.34
        self.dynamicCall("SetWMode(string)", "direct")
        self.dynamicCall("LoadMovie(long,string)", 0, url)
        self.setWindowTitle(title)
        self.hwnd = int(self.winId())

    def _reload(self, url):
        self.dynamicCall("Stop(void)")
        self.dynamicCall("LoadMove(long,string)", 0, url)


class UiNew(QtWidgets.QMainWindow):

    def __init__(self, url, title):
        super().__init__()
        self.resize(1000, 623)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(TITLE_ICON_GAME))

        self.flash = Ui_Flash(url, title)

        self.setCentralWidget(self.flash)
        self.game_hwnd = self.flash.hwnd

        self.bat_thread = None

        self.init_menu()

        # QtWidgets.qApp.focusChanged.connect(self.on_focusChanged)

    def init_menu(self):
        menubar = self.menuBar()  # 创建菜单
        # menubar.setNativeMenuBar(False)
        m_setting = menubar.addMenu('设置')

        # 给menu创建一个Action
        _reload = QtWidgets.QAction('重新登陆', self)
        _reload.setShortcut('Ctr+R')
        _reload.setStatusTip('Exit Application')
        _reload.triggered.connect(QtWidgets.qApp.quit)

        _resize = QtWidgets.QAction('恢复正常大小', self)
        _resize.triggered.connect(lambda: self.resize(1000, 623))

        set_pic = QtWidgets.QMenu('画质调整', self)
        pic_group = QtWidgets.QActionGroup(self)
        pic_high = QtWidgets.QAction('高画质', self)
        pic_high.setCheckable(True)
        pic_low = QtWidgets.QAction('低画质', self)
        pic_low.setCheckable(True)
        pic_high.triggered.connect(lambda: self.flash.dynamicCall("SetQuality2(string)", "high"))
        pic_low.triggered.connect(lambda: self.flash.dynamicCall("SetQuality2(string)", "low"))
        pic_group.addAction(pic_high)
        pic_group.addAction(pic_low)
        set_pic.addAction(pic_high)
        set_pic.addAction(pic_low)
        pic_high.setChecked(True)

        plugin_con = QtWidgets.QMenu('插件管理', self)
        self.re_framer = QtWidgets.QAction('重新雇佣', self)

        self.re_framer.triggered.connect(lambda: self.run_bat(Plugin_f(self.game_hwnd), self.re_framer))

        self.re_framer.setCheckable(True)
        plugin_con.addAction(self.re_framer)

        # 将这个Action添加到fileMenu上
        m_setting.addAction(_reload)
        m_setting.addAction(_resize)
        m_setting.addMenu(set_pic)
        m_setting.addMenu(plugin_con)

    def run_bat(self, target0, con):
        if con.isChecked() and self.bat_thread is None:
            self.bat_thread = PluginThread(target0, con)
            self.bat_thread.start()
            con.setChecked(True)
        else:
            if self.bat_thread.t.is_alive():
                print('等待线程结束')
            else:
                self.bat_thread = None
                con.setChecked(False)

    @QtCore.pyqtSlot("QWidget*", "QWidget*")
    def on_focusChanged(self, old, now):

        if now == None:
            print(f"\nwindow is the active window: {self.isActiveWindow()}")

            # window lost focus
            # do what you want0
            print(self.game_hwnd)
            try:
                pass
                self.flash.setFocus()
            except Exception as e:
                print(e)

        else:
            print(f"window is the active window: {self.isActiveWindow()}")
            pass


class flash_sa(object):
    def __init__(self, url, title):
        import os
        main = 'start plugin/flashplayer_sa'
        command = main + ' "' + url + '"'
        r_v = os.system(command)
        print(r_v)


def start_flash(url, title, run_mode):
    if run_mode == 2:
        flash_sa(url, title)
    else:
        app = QtWidgets.QApplication(sys.argv)
        ui = UiNew(url, title)
        ui.show()
        sys.exit(app.exec_())


class PostLogin(requests.Session):

    def __init__(self, account, run_mode):
        super().__init__()
        if account[0] == 1:
            self.post_login(account)
            start_flash(self.get_url(account), account[2], run_mode)
        elif account[0] == 2:
            self.post_login_7k(account)
            start_flash(self.get_url_7k(account), account[2], run_mode)

    def post_login(self, account):
        self.post(url=POST_URL_43, data=POST_4399(account[3], account[4]), headers=POST_HEADER)

    def post_login_7k(self, account):
        self.post(url=POST_URL_7k, data=POST_7K7K(account[3], account[4]), headers=POST_HEADER)

    def get_url_7k(self, acc):
        res2 = self.get(url=SERVER_7K7K(acc[1]), headers=POST_HEADER)  # 成功登陆以后，查看我们的用户数据
        soup = BeautifulSoup(res2.text, 'lxml')
        iframe_value = soup.select_one("#url").attrs["value"]

        SId = iframe_value.split('&')[2].split('=')[1]

        res3 = self.get(url=iframe_value, headers=POST_HEADER)
        soup = BeautifulSoup(res3.text, 'lxml')
        return GAME_7K7K(SId, soup.select_one("#\\37 road-ddt-game > embed").attrs["src"])

    def get_url(self, acc):
        res2 = self.get(url=SERVER_4399(acc[1]), headers=POST_HEADER)  # 成功登陆以后，查看我们的用户数据
        soup = BeautifulSoup(res2.text, 'lxml')
        iframe_src = soup.select_one("#game_box").attrs["src"]

        SId = iframe_src.split('&')[4].split('=')[1]

        res3 = self.get(iframe_src, headers=POST_HEADER)
        soup = BeautifulSoup(res3.content, 'lxml')
        return GAME_4399(SId, soup.select_one("#\\37 road-ddt-game > embed").attrs["src"])


# 模拟登陆方案
class Browser(webdriver.Chrome):
    def __init__(self, account, run_mode):
        self.has_true = False
        self.account = account
        self.run_mode = run_mode
        super().__init__(executable_path='./plugin/chromedriver')
        if account[0] == 1:
            self.do4933()
        elif account[0] == 2:
            self.do7k7k()

    def do7k7k(self):
        self.get(SERVER_7K7K(self.account[1]))
        try:
            self.find_element_by_id('username').send_keys(self.account[3])
        except:
            time.sleep(10)
            return
        self.find_element_by_id('password').send_keys(self.account[4])
        print(self.find_element_by_id('password').submit())
        for i in range(0, 100):
            time.sleep(0.5)
            if self.isElementExist('iframepage'):
                self.has_true = True
                break
        if self.has_true:
            iframe = self.find_element_by_id('iframepage')
            # //*[@id="iframepage"]
            # 切换嵌套的页面
            print(iframe.get_attribute("src"))
            self.switch_to.frame(iframe)
            self.flash = self.find_element_by_xpath('//*[@id="7road-ddt-game"]/embed')
            self.url = self.flash.get_attribute('src')
            print(self.url)
        self.quit()
        if self.has_true:
            start_flash(self.url, self.account[2], self.run_mode)

    def do4933(self):
        self.get(SERVER_4399(self.account[1]))
        try:
            self.find_element_by_id('s_user').send_keys(self.account[3])
        except:
            time.sleep(10)
            return
        self.find_element_by_id('s_password').send_keys(self.account[4])
        print(self.find_element_by_id('s_password').submit())
        for i in range(0, 100):
            time.sleep(0.5)
            if self.isElementExist('game_box'):
                self.has_true = True
                break
        if self.has_true:
            iframe = self.find_element_by_id('game_box')
            # //*[@id="game_box"]
            # //*[@id="iframepage"]
            # 切换嵌套的页面
            print(iframe.get_attribute("src"))
            self.switch_to.frame(iframe)
            self.flash = self.find_element_by_xpath('//*[@id="7road-ddt-game"]/embed')
            self.url = self.flash.get_attribute('src')
            print(self.url)
        self.quit()
        if self.has_true:
            start_flash(self.url, self.account[2], self.run_mode)

    def isElementExist(self, element):
        flag = True
        try:
            self.find_element_by_id(element)
            return flag
        except:
            flag = False
            return flag


class GameUiProcess(Process):
    def __init__(self, acc, mode, run_mode):
        Process.__init__(self)
        self.acc = acc
        self.mode = mode
        self.run_mode = run_mode

    def run(self):
        if self.mode == 2:
            Browser(self.acc, self.run_mode)
        else:
            try:
                PostLogin(self.acc, self.run_mode)
            except AttributeError:
                print('post登陆失败')
                Browser(self.acc, self.run_mode)


class AudioController(object):
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, 'has been muted.')  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, 'has been unmuted.')  # debug

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print('Volume:', interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print('Volume set to', self.volume)  # debug

    def decrease_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # 0.0 is the min value, reduce by decibels
                self.volume = max(0.0, self.volume - decibels)
                interface.SetMasterVolume(self.volume, None)
                print('Volume reduced to', self.volume)  # debug

    def increase_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # 1.0 is the max value, raise by decibels
                self.volume = min(1.0, self.volume + decibels)
                interface.SetMasterVolume(self.volume, None)
                print('Volume raised to', self.volume)  # debug
