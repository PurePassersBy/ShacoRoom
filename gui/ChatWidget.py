from PIL import ImageDraw, ImageFont, Image
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from authentication.constantName import *


def portrait_add_num(portrait_id, add_num):
    # 生成一个图像副本对象，在副本里可以对图像进行任意修改和操作
    if portrait_id is None:
        portrait_path = '../gui/resource/portrait/shaco.jpg'
    else:
        portrait_path = PORTRAIT_PATH % portrait_id
    img = Image.open(portrait_path)
    draw = ImageDraw.Draw(img)

    width, height = img.size  # 获得图像大小
    RD = min(width * 7 // 16, height * 7 // 16)  # 获得圆的直径RD
    positionC = (width - RD, 0, width, RD)       # 圆C的位置范围，图像右上角

    Red = (255, 0, 0)  # 红色
    White = "#ffffff"  # 白色
    # 加载TrueType或OpenType字体文件，并创建一个字体对象。
    if add_num >=10:
        # 添加数字大于10，数字起始位置要往左下移动，字体变小
        positionNum = (width - RD * 8 // 9, 0)  # 数字Num的起始位置
        font_size = int(RD*0.8)
    else:
        # 添加数字小于10
        positionNum = (width - RD * 3 // 4, -RD * 1 / 16)  # 数字Num的起始位置
        font_size = RD
    myfont = ImageFont.truetype('C:/windows/fonts/Arial.TTF', size=font_size)

    Add_num = str(add_num)

    draw.ellipse(positionC, fill=Red)  # 在图像的右上角画出一个红圆
    draw.text(positionNum, Add_num, font=myfont, fill=White)  # 在红圆中写出数字

    # 保存修改后的图像id+notice.jpg，原图像依然存在
    if portrait_id is None:
        portrait_path = '../gui/resource/portrait/shaco_notice.jpg'
    else:
        portrait_path = PORTRAIT_PATH % (str(portrait_id)+'notice')
    img.save(portrait_path, 'jpeg')

class BiographyWidget(QWidget):
    clicked_fetch_signal = pyqtSignal(int)
    clicked_pos_signal = pyqtSignal(int, int, int)

    def __init__(self, user_id, fetch_func=None, dialog_func=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.portrait = None
        self.num = 0
        if self.user_id is not None:
            self.clicked_fetch_signal.connect(fetch_func)
            self.clicked_pos_signal.connect(dialog_func)
        else:
            self.switch_shaco_room = fetch_func

    def hide_notice(self):
        self.num = 0
        if self.user_id is None:
            portrait_path = '../gui/resource/portrait/shaco.jpg'
        else:
            portrait_path = PORTRAIT_PATH % self.user_id
        img = QPixmap(portrait_path).scaled(30, 30)
        self.portrait.setPixmap(img)

    def show_notice(self):
        self.num += 1
        self.num = max(self.num, 99)
        portrait_add_num(self.user_id, self.num)
        if self.user_id is None:
            portrait_path = '../gui/resource/portrait/shaco_notice.jpg'
        else:
            portrait_path = PORTRAIT_PATH % (str(self.user_id)+'notice')
        img = QPixmap(portrait_path).scaled(30, 30)
        self.portrait.setPixmap(img)

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