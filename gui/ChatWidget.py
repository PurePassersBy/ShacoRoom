from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class BiographyWidget(QWidget):
    clicked_fetch_signal = pyqtSignal(int)
    clicked_pos_signal = pyqtSignal(int, int, int)

    def __init__(self, user_id, fetch_func=None, dialog_func=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        if self.user_id is not None:
            self.clicked_fetch_signal.connect(fetch_func)
            self.clicked_pos_signal.connect(dialog_func)
        else:
            self.switch_shaco_room = fetch_func

    def hide_notice(self):
        self.setStyleSheet("")

    def show_notice(self):
        self.setStyleSheet("QLabel{background-color: red;}")

    def mousePressEvent(self, QMouseEvent):
        if self.user_id is None:
            self.switch_shaco_room()
        self.clicked_fetch_signal.emit(self.user_id)
        self.clicked_pos_signal.emit(self.user_id,
                                     QMouseEvent.globalPos().x(), QMouseEvent.globalPos().y())


class BiographyLabel(QLabel):
    clicked_fetch_signal = pyqtSignal(int)
    clicked_pos_signal = pyqtSignal(int, int, int)

    def __init__(self, user_id, fetch_func, dialog_func, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.clicked_fetch_signal.connect(fetch_func)
        self.clicked_pos_signal.connect(dialog_func)

    def mousePressEvent(self, QMouseEvent):
        self.clicked_fetch_signal.emit(self.user_id)
        self.clicked_pos_signal.emit(self.user_id,
                                     QMouseEvent.globalPos().x(), QMouseEvent.globalPos().y())


class NoticeLabel(QLabel):
    clicked_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        self.clicked_signal.emit()