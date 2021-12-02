from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, \
    QLabel, QPushButton, QInputDialog, QComboBox

from utils.default import Stylesheet


class Frame(QWidget):
    list_btn = []
    plugin_dic = None

    def __init__(self, c, t, b):
        QWidget.__init__(self)
        self.cg = c
        self.set_up()
        self.title_b = t.TitleBar(self, 'DDTHelper', c.group)
        self.frame0 = b.Frame(c)
        self.init_layout()
        self.load_user()

    def sizeHint(self):
        return QSize(550, 400)

    def init_layout(self):
        layout = QVBoxLayout(self)
        # 重点： 这个widget作为背景和圆角
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout.addWidget(self.widget)

        self.lgwd = LoginConfig(self.cg)
        self.lgwd.setVisible(False)

        #
        layout0 = QHBoxLayout(self.widget)
        layout0.setSpacing(0)
        layout0.setContentsMargins(0, 0, 0, 0)  # 布局无边框

        layout0.addWidget(self.lgwd)

        main_widget = QWidget(self)
        layout1 = QGridLayout(main_widget)
        layout1.addWidget(self.title_b, 0, 0)
        layout1.addWidget(self.frame0, 1, 0)
        layout1.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum,
                                    QSizePolicy.Expanding), 2, 0)

        layout0.addWidget(main_widget)

        self.lgwd.line1.btn.clicked.connect(self.do_ontop)

        self.title_b.cb.setCurrentIndex(self.cg.group.index(self.cg.get_group_state()))

        self.title_b.cb.update_signal.connect(self.cb_event)
        self.title_b.cb.currentIndexChanged.connect(lambda: self.cb_event(0, None))
        self.title_b.cb_add.clicked.connect(lambda: self.cb_event(1, None))

    def set_up(self):
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)

    def load_user(self):
        self.frame0.add_user.clicked.connect(lambda: self.show_dialog(None))
        list0 = self.cg.group[:]
        list0.remove(self.cg.get_group_state())
        for i in self.cg.acc:
            self.frame0.add_btn(i, list0, self)

    def cb_event(self, state, msg):
        match state:
            case 3:
                if self.title_b.cb.currentText() == msg[0]:
                    self.update_frame()
                self.cg.del_team(msg[0])
            case 2:
                self.cg.rename_team(msg[0], msg[1])
            case 1:
                res, ok = QInputDialog.getText(self, "新建组", "输入队伍的名字：")
                if ok:
                    print(res)
                    self.cg.create_new_team(res)
                    self.title_b.cb.addTeam(res)
                    self.title_b.cb.setCurrentIndex(len(self.title_b.cb.list0) - 1)
                    self.update_frame()
                else:
                    self.title_b.cb.setCurrentIndex(self.cg.group.index(self.cg.get_group_state()))

            case 0:
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
        team = self.cg.data['group'][team]
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
        self.load_user()

    def wd_setting(self):
        if self.lgwd.isVisible():
            self.setFixedSize(550, 400)
            self.lgwd.setVisible(False)
        else:
            self.setFixedSize(741, 400)
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


class LoginConfig(QWidget):
    class HintButton(QWidget):
        def __init__(self, hint, text):
            super().__init__()

            layout0 = QHBoxLayout(self)

            line = QLabel(hint)
            line.setStyleSheet("color: white")
            layout0.addWidget(line)

            self.btn = QPushButton(text)
            layout0.addWidget(self.btn)

            # spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # layout0.addItem(spacer)

    class HintComboBox(QWidget):
        def __init__(self, hint, items, index=0):
            super().__init__()

            layout0 = QHBoxLayout(self)

            line = QLabel()
            line.setText(hint)
            line.setStyleSheet("color: red")
            self.cb = QComboBox()
            self.cb.addItems(items)
            self.cb.setCurrentIndex(index)

            layout0.addWidget(line)
            layout0.addWidget(self.cb)

            # spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # layout0.addItem(spacer)

    def __init__(self, cg):
        super().__init__()
        self.setFixedWidth(200)
        layout0 = QVBoxLayout(self)
        self.cg = cg

        self.line1 = self.HintButton('窗口置顶：', '否')
        self.line2 = self.HintButton('静音模启动：', '否')
        self.line3 = self.HintComboBox('游戏引擎：', ['本地', '兼容', '帮助..'], cg.data["flash"]["mode"])
        self.line4 = self.HintComboBox('游戏窗口大小:', ['默认', '小窗口', '全屏'])
        self.line5 = QPushButton('全局设置', self)

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
