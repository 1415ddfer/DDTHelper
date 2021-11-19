import time

import win32con

from utils.Plugin.onDo import *


class _main:
    name = '测试'
    hwnd = None
    state_signal = None

    def run(self):
        # 点击输入
        time.sleep(1)
        hwnd = self.hwnd
        print(hwnd)
        print(self.get_info0(self.hwnd))

    def get_info0(self, hwnd):
        # mode=[1=当前,2=公会, 3=私聊, 4=局内]
        do_click(hwnd, 58, 432)
        time.sleep(0.2)
        do_click(hwnd, 47, 531)
        time.sleep(1)
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 65)
        win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 67)
        time.sleep(0.1)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return data
