import win32api

from utils.Plugin.onDo import *


class _main:
    name = '农场重新雇人'
    hwnd = None
    state = None

    run_state = True

    def run(self):
        while True:
            self._run()
            if not self.run_state:
                break

    def _run(self):
        # 检查界面
        if get_pixel(self.hwnd, 53, 86) != '900' or get_pixel(self.hwnd, 952, 85) != '1051801':
            print('不在直顶界面')
            self.run_state = False
            return
        do_click(self.hwnd, 925, 94)
        time.sleep(0.5)
        # 清理聊天栏
        do_click(self.hwnd, 22, 480)
        time.sleep(0.5)
        # 打开界面
        do_click(self.hwnd, 454, 336)
        time.sleep(1)
        self.fire_worker()
        time.sleep(0.5)
        do_click(self.hwnd, 925, 94)
        res = self.get_worker_list()
        if not res:
            return
        # 打开界面
        do_click(self.hwnd, 477, 344)
        time.sleep(1)
        # 人才市场
        do_click(self.hwnd, 284, 120)
        time.sleep(1)
        self.get_worker(res)
        time.sleep(1)

    def fire_worker(self):
        i = 2
        while get_pixel(self.hwnd, 651, 409) == '869769':

            if get_pixel(self.hwnd, 670, 348) == '9425904':
                self.run_state = False
                print('退出')
                break
            if get_pixel(self.hwnd, 670, 348) == '2771800':
                # 第一行的员工合同没过期，开始操作第二行员工
                print('第一行的员工合同没过期，开始操作第二行员工')
                while get_pixel(self.hwnd, 651, 506) == '869769':
                    if get_pixel(self.hwnd, 669, 447) == '2177350':
                        # 第二行的员工合同没过期，结束程序
                        self.run_state = False
                        break
                    else:
                        do_click(self.hwnd, 651, 506)
                        time.sleep(0.2)
                        do_click(self.hwnd, 434, 347)
                        time.sleep(1)
                        i -= 1
                    if i == 0:
                        break
                break
            else:
                do_click(self.hwnd, 651, 409)
                time.sleep(0.5)
                do_click(self.hwnd, 434, 347)
                time.sleep(1)
                i -= 1
            if i == 0:
                break

    def get_worker_list(self):
        worker = []
        for i in str(get_info(self.hwnd, 3)).split('\r\n'):
            # 已成功解雇雇员待他一世如一
            print(i)
            if len(i) > 5 and i[4] == i[5] and i[4] == '雇':
                worker.append(i.split('员')[1])
        return worker

    def get_worker(self, list0):
        # 聚焦输入
        do_click(self.hwnd, 831, 118)
        time.sleep(0.2)
        win32api.PostQuitMessage()
        for i in list0:
            # 全选
            do_click(self.hwnd, 740, 117)
            time.sleep(0.5)
            long_position = win32api.MAKELONG(728, 118)
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDBLCLK, win32con.MK_LBUTTON, long_position)
            do_click(self.hwnd, 832, 119)
            # 粘贴数据
            # paste_to(self.control, i)
            send_to(self.hwnd, i)
            time.sleep(0.2)
            # 雇佣
            do_click(self.hwnd, 873, 118)
            time.sleep(3)
            if get_pixel(self.hwnd, 772, 276) == '6989000' or '?' in i:
                if get_pixel(self.hwnd, 870, 490) == '7317452':
                    print(i + '：搜索失败，有多个干扰')
                else:
                    while True:
                        print('进入手动模式，请操作')
                        time.sleep(1)
                        if get_pixel(self.hwnd, 870, 490) == '7317452':
                            do_click(self.hwnd, 780, 123)
                            time.sleep(2)
                            break
            else:

                print(i + '：已找到')
                do_click(self.hwnd, 826, 206)
                time.sleep(0.2)
                do_click(self.hwnd, 433, 348)
                time.sleep(0.5)
