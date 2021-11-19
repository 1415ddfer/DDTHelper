from utils.Plugin.onDo import *


class _main:

    name = '魔石合成'
    hwnd = None
    args0 = None
    state = []

    def run(self):

        while True:
            if get_pixel(self.hwnd, 308, 202) == '12578559':
                do_click(self.hwnd, 488, 324)
                time.sleep(0.2)
                send_to(self.hwnd, 'yes')
                do_click(self.hwnd, 397, 369)
                time.sleep(0.2)
                do_click(self.hwnd, 433, 345)
                time.sleep(0.5)
            else:
                break
