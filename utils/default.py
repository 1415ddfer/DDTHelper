RES_PATH = './res/'

# MainWindow
WINDOW_QSS = RES_PATH + "theme.qss"
WINDOW_ICON = RES_PATH + "win.png"
WINDOW_TITLE = "测试窗口"

WINDOW_DEFAULT_WIDTH = 640
WINDOW_DEFAULT_HEIGHT = 480

# title bar
TITLE_BAR_HEIGHT = 45
TITLE_BUTTON_SIZE = 30
TITLE_LABEL_SIZE = 30
TITLE_BUTTON_WIDTH = 25
TITLE_BUTTON_HEIGHT = 25
TITLE_ICON_MAG = 10


TITLE_MIN_ICON = RES_PATH + "min.png"
TITLE_CLS_ICON = RES_PATH + "exit.png"
TITLE_RESTORE_ICON = RES_PATH + "restore.png"
TITLE_SETTING_ICON = RES_PATH + "tool.jpeg"

TITLE_COMBOBOX_QSS = RES_PATH + "qcombobox.qss"
TITLE_ITEM_ICON = RES_PATH + "edit.png"
TITLE_ADDBTN_ICON = RES_PATH + "adduser.ico"

Stylesheet = """
#Custom_Widget {
    background: white;
    border-radius: 10px;
    background-image:url(./res/bk.jpg)
}
#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: white;
    background: red;
}
#miniButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "0";
    border-radius: 10px;
}
#miniButton:hover{
    color: white;
    background: gray;
}
"""


