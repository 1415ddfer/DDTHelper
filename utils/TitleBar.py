from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox


class TitleBar(QWidget):
    def __init__(self, parent, text, df, team):
        super(TitleBar, self).__init__()
        self.df = df
        self.win = parent
        self.team = team
        self.lay = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.lay)
        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 15, 0, 0)

        self.InitializeWindow()

    def init_team_menu(self):
        team_w = QtWidgets.QHBoxLayout()
        team_w.setSpacing(5)
        team_w.setContentsMargins(0, 0, 10, 0)  # 布局无边框

        self.cb = QComboBox()
        self.setFixedHeight(self.df.TITLE_BAR_HEIGHT)
        self.cb.setFixedSize(100, 27)
        #  self.comboBox.setCurrentIndex(2)  # 设置默认值
        # self.cb.setStyleSheet("background-color:#e7e1cc")
        print(self.team)
        self.cb.addItems(self.team)  # list
        self.cb.addItem('添加新的队伍...')
        self.cb.setStyleSheet('''
                                QComboBox{
                                    background-color:#FFFFFF;
                                    border:1px solid gray;
                                    width:300px;
                                    border-radius:10px;
                                    /* 内边框 */
                                    padding:1px 18px 1px 20px;
                                }
                                /* 当下拉框打开时,背景颜色渐变 */
                                QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                    stop: 0.5 #DDDDDD, stop: 1.0 #BBBBBB);
                                }
                                /* 下拉按钮 */
                                QComboBox::drop-down {
                                    subcontrol-origin: padding;
                                
                                    /* 按钮位置,右上角 */
                                    subcontrol-position: top right;
                                
                                    /* 按钮宽度 */
                                    width: 5px;
                                
                                
                                    /* 倒角 */
                                    border-top-right-radius: 3px;
                                    border-bottom-right-radius: 3px;
                                }
                                QComboBox::down-arrow {
                                    image: url(:/res/exit.png);
                                }

                                /* 下拉按钮位移 */
                                QComboBox::down-arrow:on {
                                    top: 1px;
                                    left: 1px;
                                }

                                /* 下拉列表里的颜色 */
                                QComboBox QAbstractItemView {
                                    border: 2px solid darkgray;
                                    selection-background-color: green;
                                }''')

        team_w.addWidget(self.cb)
        # team_w.addWidget(teamBt)
        tw = QWidget(self)
        tw.setLayout(team_w)
        # self.cb.currentIndexChanged.connect(lambda: cb_event(self))
        # self.cb.currentIndexChanged.connect(self.change_team)
        return tw

    def build_item(self, str0):
        w = QtWidgets.QWidget(self.cb)
        i_img = QtWidgets.QLabel(self)
        i_img.setPixmap(QPixmap('./res/edit.png'))
        i_img.setFixedSize(27, 27)

        i_text = QtWidgets.QLabel(self)
        i_text.setText(str0)

        i_layout = QtWidgets.QHBoxLayout(w)
        i_layout.addWidget(i_text)
        i_layout.addWidget(i_img)
        return w

    def update_cb(self, team, i):
        self.cb.clear()
        self.cb.addItems(team)
        self.cb.addItem('添加新的队伍...')
        self.cb.setCurrentIndex(i)

    def InitializeWindow(self):
        self.isPressed = False
        self.setFixedHeight(self.df.TITLE_BAR_HEIGHT)
        self.InitializeViews()
        pass

    def InitializeViews(self):
        self.iconLabel = QPushButton(self)
        self.iconLabel.setIcon(QIcon(self.df.TITLE_SETTING_ICON), )
        self.titleLabel = QLabel(self)

        tw = self.init_team_menu()

        self.minButton = QPushButton(self)
        self.closeButton = QPushButton(self)

        self.minButton.setFixedSize(self.df.TITLE_BUTTON_SIZE, self.df.TITLE_BUTTON_SIZE)
        self.closeButton.setFixedSize(self.df.TITLE_BUTTON_SIZE, self.df.TITLE_BUTTON_SIZE)

        self.iconLabel.setFixedSize(self.df.TITLE_LABEL_SIZE, self.df.TITLE_LABEL_SIZE)
        self.titleLabel.setFixedHeight(self.df.TITLE_LABEL_SIZE)

        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.minButton.setIcon(QIcon(self.df.TITLE_MIN_ICON))
        self.closeButton.setIcon(QIcon(self.df.TITLE_CLS_ICON))

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
            pix.scaled(self.iconLabel.size() - QSize(self.df.TITLE_ICON_MAG, self.df.TITLE_ICON_MAG)))

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
    def __init__(self, p):
        QComboBox.__init__(self, parent=p)
        self.setUI()

        pass

    def buildItem(self, str0):
        w = QtWidgets.QWidget(self)
        i_img = QtWidgets.QLabel(self)
        i_img.setPixmap(QPixmap('./res/edit.png'))
        i_img.setFixedSize(27, 27)

        i_text = QtWidgets.QLabel(self)
        i_text.setText(str0)

        i_layout = QtWidgets.QHBoxLayout(w)
        i_layout.addWidget(i_text)
        i_layout.addWidget(i_img)
        i_img.cl
        return w

    def setUI(self):
        self.setStyleSheet('''
                                        QComboBox{
                                            background-color:#FFFFFF;
                                            border:1px solid gray;
                                            width:300px;
                                            border-radius:10px;
                                            /* 内边框 */
                                            padding:1px 18px 1px 20px;
                                        }
                                        /* 当下拉框打开时,背景颜色渐变 */
                                        QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                                            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                            stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                            stop: 0.5 #DDDDDD, stop: 1.0 #BBBBBB);
                                        }
                                        /* 下拉按钮 */
                                        QComboBox::drop-down {
                                            subcontrol-origin: padding;

                                            /* 按钮位置,右上角 */
                                            subcontrol-position: top right;

                                            /* 按钮宽度 */
                                            width: 5px;


                                            /* 倒角 */
                                            border-top-right-radius: 3px;
                                            border-bottom-right-radius: 3px;
                                        }
                                        QComboBox::down-arrow {
                                            image: url(:/res/exit.png);
                                        }

                                        /* 下拉按钮位移 */
                                        QComboBox::down-arrow:on {
                                            top: 1px;
                                            left: 1px;
                                        }

                                        /* 下拉列表里的颜色 */
                                        QComboBox QAbstractItemView {
                                            border: 2px solid darkgray;
                                            selection-background-color: green;
                                        }''')
