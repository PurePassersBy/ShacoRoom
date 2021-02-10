
import emoji
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class EmojiLabel(QLabel):
    _signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("font:25px")
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)

    def get_init(self, emo, func):
        self.setEmoji(emo)
        self.connect_slot(func)

    def setEmoji(self, emo):
        self.emoji = emoji.emojize(emo)
        self.setText(self.emoji)

    def mousePressEvent(self, QMouseEvent):
        self._signal.emit(self.emoji)

    def connect_slot(self, func):
        self._signal.connect(func)