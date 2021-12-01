import ctypes
import inspect
import sys
import time
from functools import partial
from multiprocessing import Manager
from threading import Thread

from PyQt5.QtCore import (QThread, pyqtSignal, QObject)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QApplication, QMessageBox, QAction)

from utils.game import *
from utils.game.default import *


class Main_(QObject):
    web_voucher = None
    hwnd = None
    plugin_thread = [None, None, ]
    login_thread = None

    def __init__(self, acc, plugin, c):
        QObject.__init__(self)
        self.plugin = plugin
        self.acc = acc
        self.cf = c
        # init_thread
        self.plugin_thread_manager = Manager()

        self.app = QApplication(sys.argv)
        self.ui = UI.GameUI(acc[2], TITLE_ICON_GAME)
        self.ui.login_signal.connect(self.do_login)
        self.ui.update_state('正在登陆')
        self.do_login(0)

        self.ui.show()
        sys.exit(self.app.exec_())

    def sendMessage(self, ms):
        self.app.sendEvent(self.ui, ms)

    # 登陆类------------------------------------------------------------

    def do_login(self, s):
        if s and self.ui.layout0.count():
            self.ui.layout0.itemAt(0).widget().deleteLater()
        if self.login_thread is not None and self.login_thread.isRunning():
            print('正在运行')
        else:
            self.login_thread = LoginThread(acc=self.acc, cf=self.cf['login']['mode'])
            self.login_thread.url_signal.connect(self.login_call)
            self.login_thread.start()

    def login_call(self, s, url):
        # def get_all_child_window(parent):
        #     '''获得parent的所有子窗口句柄 返回子窗口句柄列表'''
        #     if not parent:
        #         return
        #     hwndChildList = []
        #     win32gui.EnumChildWindows(
        #         parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        #     return hwndChildList
        if s:
            if url is not None and url != '':
                self.ui.init_flash(self.cf['flash']['mode'], url)
                # self.hwnd = get_all_child_window(int(self.ui.flash_con.winId()))[1]
                self.ui.update_state('已登陆')
                # 初始化插件
                # self.init_plugin_menu()
            else:
                self.ui.update_state('登陆失败')
                # self.ui.main_text.setText('登陆失败，请检查网络或游戏维护...')
        else:
            self.ui.init_web(self.acc)
            self.ui.web.url_signal.connect(self.login_call)

    # 插件类----------------------------------------------------------
    plugin_control = pyqtSignal(int)

    def init_plugin_menu(self):
        self.ui.m_plugin.setIcon(QIcon(TITLE_PLUGIN_STOPPED))

        for key in self.plugin.keys():
            qa = QAction(key, self.ui)
            qa.triggered.connect(partial(self.run_plugin, (key, self.plugin[key])))
            self.ui.m_plugin.addAction(qa)

    def plugin_to_control(self, state, tips):
        if state == 0:
            print('重新绘制菜单')
            self.ui.m_plugin.clear()
            self.init_plugin_menu()

        self.ui.update_state(self.plugin_thread[0] + '：' + tips)

    def stop_plugin(self):
        if self.plugin_thread[1].isRunning():
            print('running')
            result = QMessageBox.information(self.ui, "提醒",
                                             "你确定要停止插件运行？",
                                             QMessageBox.Yes |
                                             QMessageBox.No)
            if result == QMessageBox.Yes:
                self.stop_thread(self.plugin_thread[1])
        else:
            print('error')
            QMessageBox.Warning(self.ui, "提示",
                                "未知错误",
                                QMessageBox.Yes)

    def run_plugin(self, list0):
        name = list0[0]
        t = list0[1]
        if self.plugin_thread is not None and self.plugin_thread[1].isRunning():
            print('运行中')
        else:
            try:
                connect_data = self.plugin_thread_manager.list([1, None])
                self.plugin_thread = [
                    name,
                    ThreadShell(self.hwnd, connect_data, None, t)
                ]
                self.plugin_thread.append(ThreadBrother(self.plugin_thread[1], connect_data))
                self.plugin_thread[2].state_signal.connect(self.plugin_to_control)
                self.plugin_thread[1].start()
                self.plugin_thread[2].start()
                # 菜单变形
                self.ui.m_plugin.clear()
                a = QAction('停止插件', self.ui)
                self.ui.m_plugin.addAction(a)
                a.triggered.connect(self.stop_plugin)
            except Exception as e:
                print(e)

    @staticmethod
    def stop_thread(thread):
        def _async_raise(tid, exc_type):
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exc_type):
                exc_type = type(exc_type)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        _async_raise(thread.ident, SystemExit)


class ThreadBrother(QThread):
    def __init__(self, t=Thread(target=None), state=None):
        QThread.__init__(self)
        self.t = t
        self.state = state

    state_signal = pyqtSignal(int, str)

    def run(self):
        self.state_signal.emit(1, '正在运行')
        list_old = []
        while self.t.is_alive():
            if self.state != list_old:
                list_old = self.state
                self.state_signal.emit(list_old[0], list_old[1])
                time.sleep(0.5)
            else:
                time.sleep(1)

        self.state_signal.emit(0, '已停止运行')


class ThreadShell(Thread):
    def __init__(self, hwnd=None, state=None, args0=None, ojb=None):
        Thread.__init__(self)
        ojb.hwnd = hwnd
        ojb.args = args0
        ojb.state = state
        self.ojb = ojb
        self.state = state

    def run(self):
        try:
            self.ojb.run()
        except Exception as e:
            print(e)


class LoginThread(QThread):

    def __init__(self, flag=None, acc=None, cf=None):
        QThread.__init__(self)
        self.state = True
        self.acc = acc
        self.cf = cf
        self.flag = flag

    url_signal = pyqtSignal(int, str)

    def run(self):
        res = self.login_()
        if res:
            self.url_signal.emit(1, res)

    def login_qweb(self):
        self.url_signal.emit(0, None)

    def login_(self):
        if self.cf[0] == 2:
            self.login_qweb()
            return 0
        else:
            try:
                post_login = login.PostLogin(self.acc)
                match self.acc[0]:
                    case 1:  # 登陆到4399
                        post_login.post_login()
                        return post_login.get_url()

                    case 2:  # 登陆到7k7k
                        post_login.post_login_7k()
                        return post_login.get_url_7k()

                    case 3:  # 登陆到7道
                        self.login_qweb()
                        return 0

            except AttributeError as e:
                print('post登陆失败')
                print(e)
                self.login_qweb()
                return 0
            except login.requests.exceptions.ConnectionError:
                print('当前没有网络连接')
                QMessageBox.critical(None, '错误', '当前没有网络连接', QMessageBox.Yes, QMessageBox.Yes)
                return 0
