
import emoji
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.VEmojiWindow import Ui_Dialog

EMOJI_LIST = [':simple_smile:', ':smile:', ':laughing:', ':smirk:', ':anguished:', ':open_mouth:',
              ':angry:', ':scream:', ':sob:', ':sunglasses:', ':imp:', ':alien:', ':thumbs_up:',
              ':thumbs_down:', ':ok_hand:']

class EmojiWindow(QWidget, Ui_Dialog):
    emoji_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    for emo in EMOJI_LIST:
        print(emoji.emojize(emo))

    print(emoji.emojize("U+1F600"))


