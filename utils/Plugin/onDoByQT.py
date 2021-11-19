import time

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent, QMouseEvent


def doClick(app, con, pos):
    key = Qt.LeftButton
    pos = QPoint(pos)
    state = Qt.NoModifier
    app.sendEvent(con, QMouseEvent(QMouseEvent.MouseButtonPress, pos, key, state))
    app.sendEvent(con, QMouseEvent(QMouseEvent.MouseButtonRelease, pos, key, state))


def do_fire_for_time(app, con, power):
    key = Qt.Key_Space
    state = Qt.NoModifier
    # 按下
    app.sendEvent(con, QKeyEvent(QKeyEvent.KeyPress, key, state))
    time.sleep(power * 0.04)
    # 松开
    app.sendEvent(con, QKeyEvent(QKeyEvent.KeyRelease, key, state))
