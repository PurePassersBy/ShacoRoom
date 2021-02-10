import sys

import emoji
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.VEmojiWindow import Ui_emoji

EMOJI_LIST = [':clown_face:', ':grinning_face_with_big_eyes:', ':beaming_face_with_smiling_eyes:',
              ':grinning_face_with_sweat:', ':face_with_tears_of_joy:', ':rolling_on_the_floor_laughing:',
              ':upside-down_face:',':smiling_face_with_hearts:', ':face_savoring_food:', ':shushing_face:',
              ':expressionless_face:', ':sleeping_face:', ':face_vomiting:', ':face_with_symbols_on_mouth:',
              ]


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


class EmojiWindow(QWidget, Ui_emoji):
    emoji_signal = pyqtSignal(str)

    def __init__(self, emoji_list=None):
        super().__init__()
        self.setupUi(self)
        if emoji_list is None:
            self.emoji_list = EMOJI_LIST
        for i in range(len(self.emoji_list)):
            if i == 0:
                code = 'self.label.get_init("%s", self.send_emoji_signal)' % self.emoji_list[i]
            else:
                code = 'self.label_%d.get_init("%s", self.send_emoji_signal)' % (i+1, self.emoji_list[i])
            exec(code)

    def send_emoji_signal(self, emoji):
        self.close()
        self.emoji_signal.emit(emoji)

    def connect_slot(self, func):
        self.emoji_signal.connect(func)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()  # 点击其他程序窗口，会关闭该对话框
            return True
        else:
            return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    emoji_window = EmojiWindow()
    emoji_window.show()
    sys.exit(app.exec_())


