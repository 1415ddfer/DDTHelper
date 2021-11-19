from PyQt5 import QtWidgets


class ConfigBox(QtWidgets.QTabWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('设置')
        self.setFixedSize(550, 350)
        self.init_tab()

    def init_tab(self):
        tab0 = ConfigMain()
        self.addTab(tab0, '主要配置')


class ConfigMain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout0 = QtWidgets.QVBoxLayout()

        self.cb0 = QtWidgets.QCheckBox()
        self.cb0.setText('启动器始终置顶')

        self.cb1 = HintComboBox('启动器风格：', ['默认', '经典'])
        self.cb2 = HintComboBox('登陆模式：', ['默认（先Post失败调用浏览器)', '只使用用Post登陆', '只使用浏览器登陆'])

        bt_about = QtWidgets.QPushButton('关于v.043')
        line = QtWidgets.QLabel('Power by DDF')

        layout0.addWidget(self.cb0)
        layout0.addWidget(self.cb1)
        layout0.addWidget(self.cb2)
        layout0.addWidget(bt_about)
        layout0.addWidget(line)

        self.setLayout(layout0)



class HintComboBox(QtWidgets.QWidget):
    def __init__(self, hint, items):
        super().__init__()

        layout0 = QtWidgets.QHBoxLayout(self)

        line = QtWidgets.QLabel()
        line.setText(hint)
        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(items)

        layout0.addWidget(line)
        layout0.addWidget(self.cb)

        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout0.addItem(spacer)
