from PyQt5.QtCore import Qt, QSize, pyqtSignal, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QDialog, QLineEdit, \
    QListWidgetItem, QToolButton, QListWidget, QMessageBox

from utils.default import *


class TitleBar(QWidget):
    def __init__(self, parent, text, team):
        super(TitleBar, self).__init__()
        self.win = parent
        self.team = team
        self.lay = QHBoxLayout(self)
        self.setLayout(self.lay)
        self.lay.setSpacing(0)
        self.setFixedHeight(30)
        self.lay.setContentsMargins(20, 0, 20, 0)

        self.InitializeWindow()

    def init_team_menu(self):
        team_w = QHBoxLayout()
        team_w.setSpacing(0)
        team_w.setContentsMargins(0, 0, 25, 0)  # 布局无边框

        self.cb = TeamMenu(self)
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self.cb.setFixedSize(120, 30)
        for i in self.team:
            self.cb.addTeam(i)

        self.cb_add = QToolButton(self)
        self.cb_add.setIcon(QIcon(TITLE_ADDBTN_ICON))
        self.cb_add.setIconSize(QSize(27, 27))
        self.cb_add.setFixedSize(30, 30)

        team_w.addWidget(self.cb)
        team_w.addWidget(self.cb_add)
        tw = QWidget(self)
        tw.setLayout(team_w)
        return tw

    def update_cb(self, team, i):
        self.cb.clear()
        for i in team:
            self.cb.addTeam(i)
        self.cb.setCurrentIndex(i)

    def InitializeWindow(self):
        self.isPressed = False
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self.InitializeViews()

    def InitializeViews(self):
        self.iconLabel = QPushButton(self)
        self.iconLabel.setIcon(QIcon(TITLE_SETTING_ICON), )
        self.titleLabel = QLabel(self)

        tw = self.init_team_menu()

        self.minButton = QPushButton(self)
        self.closeButton = QPushButton(self)

        self.minButton.setFixedSize(TITLE_BUTTON_SIZE, TITLE_BUTTON_SIZE)
        self.closeButton.setFixedSize(TITLE_BUTTON_SIZE, TITLE_BUTTON_SIZE)

        self.iconLabel.setFixedSize(TITLE_LABEL_SIZE, TITLE_LABEL_SIZE)
        self.titleLabel.setFixedHeight(TITLE_LABEL_SIZE)

        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.minButton.setIcon(QIcon(TITLE_MIN_ICON))
        self.closeButton.setIcon(QIcon(TITLE_CLS_ICON))

        self.iconLabel.clicked.connect(self.win.wd_setting)
        self.minButton.clicked.connect(self.ShowMininizedWindow)
        self.closeButton.clicked.connect(self.CloseWindow)

        self.lay.addWidget(self.iconLabel)
        self.lay.addWidget(self.titleLabel)
        self.lay.addWidget(tw)
        self.lay.addWidget(self.minButton)
        self.lay.addWidget(self.closeButton)

    def ShowMininizedWindow(self):
        self.win.showMinimized()

    def ShowMaximizedWindow(self):
        self.win.showMaximized()

    def CloseWindow(self):
        self.win.close()

    def SetTitle(self, str):
        self.titleLabel.setText(str)

    def SetIcon(self, pix):
        self.iconLabel.setPixmap(
            pix.scaled(self.iconLabel.size() - QSize(TITLE_ICON_MAG, TITLE_ICON_MAG)))

    # def mouseDoubleClickEvent(self, event):
    #     self.ShowRestoreWindow()
    #     return QWidget().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.isPressed = True
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPressed:
            if self.win.isMaximized:
                self.win.showNormal()

            movePos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            self.win.move(self.win.pos() + movePos)

        return QWidget().mouseMoveEvent(event)


class TeamMenu(QComboBox):
    list0 = []
    list1 = []

    def __init__(self, p):
        QComboBox.__init__(self, parent=p)
        self.m_list = QListWidget(self)
        self.setModel(self.m_list.model())
        self.setView(self.m_list)

        self.setQss(TITLE_COMBOBOX_QSS, self)

    update_signal = pyqtSignal(int, list)

    @staticmethod
    def setQss(file, control):
        with open(file, mode='r', encoding='UTF-8') as f:
            qss = f.read()
            control.setStyleSheet(qss)

    def setTeamList(self, l0):
        self.addItems(l0)
        for i in l0:
            self.addTeam(i)

    def clearTeam(self):
        self.m_list.clear()
        self.list0 = []
        self.list1 = []

    def addTeam(self, text):
        self.list0.append(text)
        item = ComboBoxItem(len(self.list0) - 1)
        item.itemOpSignal.connect(self.editTeam)
        _w = QListWidgetItem(self.m_list)
        _w.setText(text)
        self.list1.append(_w)
        self.m_list.setItemWidget(_w, item)

    def editTeam(self, i):
        inp = EditDialog(self, self.list0[i])
        inp.res_signal.connect(self.changeTeam)
        inp.show()

    def changeTeam(self, state, str0, str1):
        i = self.list0.index(str0)
        if state:
            self.update_signal.emit(2, [str0, str1])
            self.list0[i] = str1
            self.list1[i].setText(str1)
        else:
            if len(self.list0) - 1:
                self.update_signal.emit(3, [str0])
                self.m_list.takeItem(i)
                del self.list0[i]
                del self.list1[i]
            else:
                QMessageBox.information(self, "提示", "当只有一个队列时不可删除",
                                        QMessageBox.Yes)


class EditDialog(QDialog):
    def __init__(self, p, name):
        QDialog.__init__(self, p)
        self.name = name
        self.layout0 = QVBoxLayout(self)

        i_w = QWidget(self)
        i_l = QHBoxLayout(i_w)

        i_l.addWidget(QLabel('队伍名字：', self))

        self.ed = QLineEdit(name, self)
        i_l.addWidget(self.ed)

        del_btn = QPushButton(self)
        del_btn.setFixedSize(16, 16)
        del_btn.setIcon(QIcon(TITLE_CLS_ICON))
        del_btn.clicked.connect(self.del_data)
        i_l.addWidget(del_btn)

        m_w = QWidget(self)
        m_l = QHBoxLayout(m_w)

        btn_no = QPushButton('取消', self)
        btn_no.clicked.connect(self.close)
        m_l.addWidget(btn_no)

        btn_yes = QPushButton('确定', self)
        btn_yes.clicked.connect(self.upload)
        m_l.addWidget(btn_yes)

        self.layout0.addWidget(i_w)
        self.layout0.addWidget(m_w)

    res_signal = pyqtSignal(int, str, str)

    def del_data(self):
        msg = QMessageBox.warning(self, "提示", "确实要删除队伍吗?",
                                  QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.res_signal.emit(0, self.name, None)
            self.close()

    def upload(self):
        self.res_signal.emit(1, self.name, self.ed.text())
        self.close()


class ComboBoxItem(QWidget):
    def __init__(self, index):
        super().__init__()
        self.cbIndex = index
        self.layout0 = QHBoxLayout(self)
        self.layout0.setContentsMargins(10,  # left
                                        0,  # end
                                        10,  # right
                                        0)  # top

        self.lb_text = QLabel(self)
        self.bt_close = QToolButton(self)
        self.bt_close.setIcon(QIcon(TITLE_ITEM_ICON))
        self.bt_close.setAutoRaise(True)

        self.layout0.addWidget(self.lb_text)
        self.layout0.addWidget(self.bt_close)

        # 布局内容省略

        self.bt_close.installEventFilter(self)
        self.installEventFilter(self)

    itemOpSignal = pyqtSignal(int)

    # 事件拦截
    def eventFilter(self, object, event):
        if object is self:
            if event.type() == QEvent.Enter:
                self.setStyleSheet("QWidget{color:white}")
            elif event.type() == QEvent.Leave:
                self.setStyleSheet("QWidget{color:black}")
        elif object is self.bt_close:
            if event.type() == QEvent.MouseButtonPress:
                self.itemOpSignal.emit(self.cbIndex)
        return QWidget.eventFilter(self, object, event)
