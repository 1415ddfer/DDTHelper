import math
from multiprocessing import Process

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu, QSpacerItem, QSizePolicy


class BtnMenu(QMenu):
    m_item = []

    def __init__(self, group):
        super().__init__()
        # 创建QMenu
        self.m_edit = self.contextMenu.addAction('编辑')
        self.m_del = self.contextMenu.addAction('删除')
        # 二级菜单
        self.m_group = self.contextMenu.addMenu("移动到分组")
        for i in group:
            self.m_item.append(self.m_group.addAction(i))


class MenuButton(QPushButton):
    m_process = None

    def __init__(self, parent, acc_group, user, wd):
        super(MenuButton, self).__init__(parent)
        self.contextMenu = QMenu(self)
        self.acc_group = acc_group
        self.user = user
        self.wd = wd
        self.setText(str(self.user[1]) + '-' + self.user[2])
        self.setMaximumSize(70, 70)
        self.setMinimumSize(70, 70)
        self.m_item = []
        self.init_menu()

        self.clicked.connect(self.start_game_new)

    def init_menu(self):
        """''
                            创建右键菜单
        """
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 创建QMenu
        self.m_edit = self.contextMenu.addAction('编辑')
        self.m_del = self.contextMenu.addAction('删除')
        # 二级菜单
        self.m_group = self.contextMenu.addMenu("移动到分组")
        for i in self.acc_group:
            self.m_item.append(self.m_group.addAction(i))
            self.m_item[-1].triggered.connect(lambda: self.wd.moveto_other_team(self.user, 'team'))
        # 事件绑定
        self.m_edit.triggered.connect(lambda: self.wd.show_dialog(self.user))
        self.m_del.triggered.connect(lambda: self.wd.del_data(self.user))

    def show_context_menu(self):
        """''
        右键点击时调用的函数
        """
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def start_game_new(self):
        if self.m_process is not None and self.m_process.is_alive():
            print('线程运行中')
        else:
            try:
                from utils.game import new_main
                self.m_process = Process(target=new_main.Main_,
                                         args=(self.user, self.wd.plugin_dic, self.wd.cg.data))
                self.m_process.start()
            except Exception as e:
                print(e)

        # 0为使用cookiePost，1使用账号post，2使用chrome登陆
        # v3.0 移除cookiePost


class Frame(QWidget):
    list_btn = []
    m_process = None

    def __init__(self, c):
        super(Frame, self).__init__()
        self.cf = c

        self.layout0 = QtWidgets.QGridLayout()
        self.layout0.setSpacing(30)
        self.setLayout(self.layout0)
        self.set_up()

    def set_up(self):
        self.add_user = QtWidgets.QPushButton('添加', self)
        self.add_user.setStyleSheet('''
            QPushButton{
                background-color: #d4b4d7;
                border: 1px solid gray;
                border-radius: 20px;
            }
            QPushButton:hover { color: blue }
            QPushButton:hover:!pressed { color: white }''')
        self.add_user.setMinimumSize(60, 60)
        self.add_user.setMaximumSize(60, 60)
        self.layout0.addWidget(self.add_user, 0, 0)
        self.layout0.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 5)
        # add_btn.setGeometry(QtCore.QRect(15, 15, 60, 60))
        # add_btn.clicked.connect(lambda: self.show_dialog(None))

    def add_btn(self, user, group, wd):
        i = len(self.list_btn) + 1
        btn = MenuButton(None, group, user, wd)
        btn.setStyleSheet('''
            QPushButton{
                background-color: #d4b4d7;
                border: 1px solid gray;
                border-radius: 20px;
            }
            QPushButton:hover { color: blue }
            QPushButton:hover:!pressed { color: white }''')
        btn.setFixedSize(70, 70)
        self.list_btn.append(btn)
        self.layout0.addWidget(btn, math.floor(i / 4), i % 4)

        # btn.clicked.connect(lambda: self.start_game(user))  # 绑定按钮点击事件
        # btn.m_edit.triggered.connect(lambda: self.show_dialog(self.cg.acc[i]))

        QApplication.processEvents()

    def reload_self(self):
        for i in range(self.layout0.count()):
            self.layout0.itemAt(i).widget().deleteLater()
        self.list_btn = []
        self.set_up()
