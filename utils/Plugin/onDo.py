import time
from urllib import parse

import numpy as np
from PIL import Image

import win32api
import win32clipboard
import win32con
import win32gui
import win32ui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication

IS_IN_LOBBY = [[103, 120, 340499], [116, 119, 1079727]]
IS_IN_GAME = [[958, 12, 5153375], [111, 578, 15853770]]
IS_IN_ROOM_FB = [[802, 29, 53247], [517, 418, 10928328]]
IS_IN_ROOM_PK = [[802, 29, 53247], [517, 418, 8765128]]


def This_is_where(hwnd, where):
    is_its = True
    for i in where:
        if is_its:
            is_its = get_pixel(hwnd, i[0], i[1]) == i[2]
        else:
            return False
    return True


class MyException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


def h2tos(data='', mode=0):
    """str0:传入的数据, mode=1为将字符转成hex"""
    if mode:
        return parse.quote(data).replace('%', ' ')
    else:
        return parse.unquote('%' + data.replace(' ', '%'))


def get_all_child_window(parent):
    '''获得parent的所有子窗口句柄 返回子窗口句柄列表'''
    if not parent:
        return
    hwndChildList = []

    win32gui.EnumChildWindows(
        parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList


def get_image_for_window(hwnd):
    screen = QApplication.primaryScreen()

    img = screen.grabWindow(hwnd).toImage()
    cropped = img[0:128, 0:512]  # 裁剪坐标为[y0:y1, x0:x1]

    cropped.save("screenshot.jpg")


def check(hwnd, cx, cy, cool):
    hdc = win32gui.GetWindowDC(hwnd)
    i = 0
    while str(win32gui.GetPixel(hdc, cx, cy)) != str(cool):  # 房间检测
        print("检查房间")
        do_click(hwnd, 5, 5)
        time.sleep(1)
        i += 1
        if i > 10:
            raise MyException('检查房间操作超时，请检查游戏状态')


def climb(hwnd, jl, fx):
    if fx == 1:  # 右边
        # 适应方向及防止无效
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 68, None)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 68, None)
        # 1.3=1屏距
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 68, None)
        time.sleep(jl * 1.3)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 68, None)
    else:
        # 适应方向及防止无效
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 65, None)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 65, None)
        # 1.3=1屏距
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 65, None)
        time.sleep(jl * 1.3)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 65, None)


def do_angle(hwnd, jd):
    for i in range(jd):
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 87, None)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 87, None)


def do_click(hwnd, cx, cy):
    long_position = win32api.MAKELONG(cx, cy)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)


def do_fire(hwnd, ld):
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 66, None)  # 先摁大
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 69, None)  # 先摁技能
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 97, None)
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 98, None)
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 97, None)  # 11大招
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 100, None)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 32, None)
    time.sleep(ld * 0.04)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 32, None)


def do_fire_tmp(hwnd, ld):
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 97, None)  # 11大招
    win32api.PostMessage(hwnd, win32con.WM_KEYFIRST, 100, None)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 32, None)
    time.sleep(ld * 0.04)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 32, None)


def keep_fire(hwnd, ld):
    while True:
        cs = 0
        while get_pixel(hwnd, 497, 169) != str(5418993):  # 回合检测
            if cs >= 20:  # 超时退出
                break
            else:
                time.sleep(1)
                cs = cs + 1
        if cs == 20:
            print("退出副本")
            break
        else:
            do_fire(hwnd, ld)


def get_pixel(hwnd, cx, cy):
    do_click(hwnd, 5, 5)
    time.sleep(0.2)
    return str(win32gui.GetPixel(win32gui.GetWindowDC(hwnd), cx, cy))


def send_to(hwnd, data):
    for i in data:
        win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(i), 0)


def get_info(hwnd, mode):
    # mode=[1=当前,2=公会, 3=私聊, 4=局内]
    if mode == 4:
        pass
    else:
        if get_pixel(hwnd, 17, 456) == '3572948':
            time.sleep(0.2)
            do_click(hwnd, 18, 464)
        if mode == 2:
            time.sleep(0.2)
            do_click(hwnd, 141, 424)
        elif mode == 3:
            time.sleep(0.2)
            do_click(hwnd, 221, 428)
        else:
            do_click(hwnd, 58, 432)
        # start_p = win32api.MAKELONG(35, 475 + 20*(line-1))
        # end_p = win32api.MAKELONG(474, 555)
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
    win32clipboard.EmptyClipboard()  # 清理数据
    win32clipboard.CloseClipboard()
    return data


def shot(hwnd, sx, sy, ex, ey):
    """
        根据窗口句柄截取窗口视图
    :param hwnd: 窗口句柄 一个整数
    """

    def Hex_to_RGB(hex):
        r = int(hex[1:3], 16)
        g = int(hex[3:5], 16)
        b = int(hex[5:7], 16)
        return [r, g, b]

    def RGB_to_Hex(rgb):
        color = '#'
        for i in rgb:
            num = int(i)
            # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
            color += str(hex(num))[-2:].replace('x', '0').upper()
        print(color)
        return color

    # 获取后台窗口的句柄，注意后台窗口不能最小化
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    # 保存bitmap到文件
    # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)

    cropped = im_PIL.crop((sx, sy, ex, ey))  # (left, upper, right, lower)
    cropped.save("./pil_cut_thor.jpg")

    pic = cropped.convert('L')
    pic.save('test2')

    def pic_l(tmp):
        tmp = cropped.convert('L').getdata()
        data = np.array(tmp)
        print(data)

        for i in range(len(data + 1)):
            if data[i] == 67:
                data[i] = 255
            else:
                data[i] = 0
        photo = Image.fromarray(np.uint8(data), 'L')
        photo.save("test2.jpg")
