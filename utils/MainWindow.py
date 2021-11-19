from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox
from utils.Plugin.Loader import LoadPlugin


class Frame(QWidget, LoadPlugin):
    list_btn = []

    def __init__(self, c, d, t, b):
        QWidget.__init__(self)
        self.cg = c
        self.set_up()
        self.title_b = t.TitleBar(self, 'DDTHelper', d, c.group)
        self.frame0 = b.Frame(c)
        self.init_layout()
        self.load_user()

    def init_layout(self):
        layout_0 = QtWidgets.QHBoxLayout(self)
        layout_0.setSpacing(0)
        layout_0.setContentsMargins(0, 0, 0, 0)  # 布局无边框

        self.lgwd = LoginConfig(self.cg)
        self.lgwd.setVisible(False)
        layout_0.addWidget(self.lgwd)

        wd1 = QtWidgets.QWidget()
        layout_1 = QtWidgets.QVBoxLayout(wd1)  # 全局竖直
        layout_0.addWidget(wd1)

        self.frame0.setStyleSheet("background-color:#cdbb92")

        layout_1.addWidget(self.title_b)  # 四个部件加至全局布局
        layout_1.addWidget(self.frame0)

        layout_1.setSpacing(0)
        layout_1.setContentsMargins(0, 0, 0, 0)  # 布局无边框

        self.lgwd.line1.btn.clicked.connect(self.do_ontop)

        self.title_b.cb.setCurrentIndex(self.cg.group.index(self.cg.get_group_state()))

        self.title_b.cb.currentIndexChanged.connect(lambda: self.cb_event())

    def set_up(self):
        self.setFixedSize(450, 350)  # 450+50|350-20
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去除默认标题栏
        font = QtGui.QFont()
        font.setFamily("微软雅黑")

    def load_user(self):
        self.frame0.add_user.clicked.connect(lambda: self.show_dialog(None))
        list0 = self.cg.group[:]
        list0.remove(self.cg.get_group_state())
        for i in self.cg.acc:
            self.frame0.add_btn(i, list0, self)

    def cb_event(self):
        print(self.title_b.cb.currentText())
        if self.title_b.cb.currentText() == '添加新的队伍...':
            res, ok = QtWidgets.QInputDialog.getText(self, "新建组", "输入队伍的名字：")
            if ok:
                try:
                    print(res)
                    i = self.title_b.cb.currentIndex()
                    self.cg.create_new_team(res)
                    self.title_b.update_cb(self.cg.group, i)
                    self.update_frame()
                except Exception as e:
                    print(e)
            else:
                self.title_b.cb.setCurrentIndex(self.cg.group.index(self.cg.get_group_state()))
        else:
            self.update_frame()

    def show_dialog(self, data):
        from utils import showDialog
        res = showDialog.inputDialog.on_run(data)
        if res is not None:
            if data is not None:
                self.cg.rewrite_data(res, data[3])
            else:
                self.cg.add_data(res, None)
            self.update_frame()

    def moveto_other_team(self, user, team):
        team = team.text()
        print(team)
        td = QMessageBox.warning(self, "提示", "确实要移动吗?",
                                 QMessageBox.Yes | QMessageBox.No)
        if td == QMessageBox.Yes:
            self.cg.del_user(user)
            self.cg.add_data(user, team)
            self.update_frame()

    def del_data(self, user):
        td = QMessageBox.warning(self, "提示", "确实要删除吗?",
                                 QMessageBox.Yes | QMessageBox.No)
        if td == QMessageBox.Yes:
            self.cg.del_user(user)
            self.update_frame()

    def update_frame(self):
        data = self.title_b.cb.currentText()
        self.cg.init_team(data)
        self.frame0.reload_self()
        try:
            self.load_user()
        except Exception as e:
            print(e)

    def wd_setting(self):
        if self.lgwd.isVisible():
            self.setFixedSize(450, 350)
            self.lgwd.setVisible(False)
        else:
            self.setFixedSize(650, 350)
            self.lgwd.setVisible(True)

    def do_ontop(self):
        btn = self.lgwd.line1.btn
        if btn.text() == '否':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            btn.setText('是')
            self.setVisible(True)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
            btn.setText('否')
            self.setVisible(True)


class LoginConfig(QtWidgets.QWidget):
    class HintButton(QtWidgets.QWidget):
        def __init__(self, hint, text):
            super().__init__()

            layout0 = QtWidgets.QHBoxLayout(self)

            line = QtWidgets.QLabel(hint)
            layout0.addWidget(line)

            self.btn = QtWidgets.QPushButton(text)
            layout0.addWidget(self.btn)

            # spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # layout0.addItem(spacer)

    class HintComboBox(QtWidgets.QWidget):
        def __init__(self, hint, items, index=0):
            super().__init__()

            layout0 = QtWidgets.QHBoxLayout(self)

            line = QtWidgets.QLabel()
            line.setText(hint)
            self.cb = QtWidgets.QComboBox()
            self.cb.addItems(items)
            self.cb.setCurrentIndex(index)

            layout0.addWidget(line)
            layout0.addWidget(self.cb)

            # spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # layout0.addItem(spacer)

    def __init__(self, cg):
        super().__init__()
        self.setFixedWidth(200)
        layout0 = QtWidgets.QVBoxLayout(self)
        self.cg = cg

        self.line1 = self.HintButton('窗口置顶：', '否')
        self.line2 = self.HintButton('静音模启动：', '否')
        self.line3 = self.HintComboBox('游戏引擎：', ['本地', '兼容', '帮助..'], cg.data["flash"]["mode"])
        self.line4 = self.HintComboBox('游戏窗口大小:', ['默认', '小窗口', '全屏'])
        self.line5 = QtWidgets.QPushButton('全局设置', self)

        layout0.addWidget(self.line1)
        layout0.addWidget(self.line2)
        layout0.addWidget(self.line3)
        layout0.addWidget(self.line4)
        layout0.addWidget(self.line5)

        self.line3.cb.currentIndexChanged.connect(self.set_flashMode)

    def set_flashMode(self):
        a = self.line3.cb.currentIndex()
        if a == 2:
            print('building')
            self.line3.cb.setCurrentIndex(self.cg.data["flash"]["mode"])
            return

        self.cg.data["flash"]["mode"] = a
