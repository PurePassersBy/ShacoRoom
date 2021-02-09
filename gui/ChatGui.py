import sys
import os
import pickle
import struct
from time import sleep
import threading
import socket

import numpy as np
from PIL import Image, ImageQt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

sys.path.append('..')
from gui.VChat import Ui_Form
from gui.SettingsGui import SettingsGui
from authentication.dialogGUI import Dialog
from authentication.dialogGUI import Biography

SERVER_IP = '39.106.169.58'
SERVER_ADDRESS = ('39.106.169.58', 3976)
VIDEO_SERVER_ADDRESS = ('39.106.169.58', 3977)
AUDIO_SERVER_ADDRESS = ('39.106.169.58', 3978)
RESOURCE_SERVER_ADDRESS = ('39.106.169.58', 3979)
PORTRAIT_PATH = '../gui/resource/portrait/%s.jpg'
TABLE_NAME = 'userinfo'
LINE_LENGTH = 39
UNI2ASC = 40 / 24
message_lock = threading.Lock()

def split_message(msg):
    msg_list = []
    size = 0; now = ''
    for char in msg:
        size += 1 if ord(char)<128 else UNI2ASC
        now += char
        if size > LINE_LENGTH:
            msg_list.append(now)
            size = 0; now = ''
    if len(now) > 0:
        msg_list.append(now)
    return msg_list


def send_package(conn, pack):
    pack_str = pickle.dumps(pack)
    conn.send(struct.pack('i', len(pack_str)))
    conn.send(pack_str)


def fetch_package(conn):
    size = struct.unpack('i', conn.recv(4))[0]
    data = ''.encode()
    while len(data) < size:
        if len(data) + 2048 > size:
            data += conn.recv(size - len(data))
        else:
            data += conn.recv(2048)
    pack = pickle.loads(data)
    return pack


class Portrait(QLabel):
    clicked_signal = pyqtSignal(int)
    clicked_pos_signal = pyqtSignal(int, int, int)

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id

    def mousePressEvent(self, QMouseEvent):
        self.clicked_signal.emit(self.user_id)
        self.clicked_pos_signal.emit(self.user_id,
                                     QMouseEvent.globalPos().x(), QMouseEvent.globalPos().y())

    def connect_pos_slot(self, func):
        self.clicked_pos_signal.connect(func)

    def connect_customized_slot(self, func):
        self.clicked_signal.connect(func)


class ReceiveMessageThread(QThread):
    msg_pack = pyqtSignal(dict)

    def __init__(self, chatter):
        super().__init__()
        self.chatter = chatter

    def run(self):
        while True:
            try:
                pack = fetch_package(self.chatter)
                self.msg_pack.emit(pack)
                sleep(0.1)
            except Exception as e:
                print('Receiver Message Error', e)
                break


class ChatGUI(QWidget, Ui_Form):

    def __init__(self, user_id, user_name, fav_comic, is_know, db_conn):
        super(ChatGUI, self).__init__()
        self.setupUi(self)

        icon = QIcon()
        icon.addPixmap(QPixmap("../gui/resource/shaco_logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.emoji_button.setIcon(QIcon("../gui/resource/button/emoji_button.png"))
        self.emoji_button.setIconSize(QSize(39,28))
        self.image_button.setIcon(QIcon("../gui/resource/button/image_button.png"))
        self.image_button.setIconSize(QSize(39, 28))
        self.file_button.setIcon(QIcon("../gui/resource/button/file_button.png"))
        self.file_button.setIconSize(QSize(39, 28))

        self.id = user_id
        self.userName = user_name
        self.portrait = f'../gui/resource/portrait/{self.id}.jpg'
        self.favComic = fav_comic
        self.isKnow = is_know
        self._flush()

        self.db_conn = db_conn

        self.init_client()

        self.textEdit.installEventFilter(self)

        # 初始化登出或登录通知
        self.dialog = None
        # 初始化个人简介页面
        self.biography = None



    def _fetch_others_portrait(self, user_id):
        query = {
            'type': 'fetch',
            'user_id': user_id
        }
        send_package(self.portrait_client, query)
        header = fetch_package(self.portrait_client)
        file_size = header['file_size']
        print(f'接收 {user_id} 的头像，大小为{file_size}')
        if file_size == 0:
            return
        file_path = f'../gui/resource/portrait/{user_id}.jpg'
        with open(file_path, 'wb') as f:
            recv_size = 0
            while recv_size < file_size:
                if recv_size + 1024 > file_size:
                    data = self.portrait_client.recv(file_size - recv_size)
                else:
                    data = self.portrait_client.recv(1024)
                f.write(data)
                recv_size += len(data)
        print('接收成功')

    def init_client(self):
        self.chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatter.connect(SERVER_ADDRESS)
        header = {
            'user_id': self.id,
            'user_name': self.userName
        }
        message_lock.acquire()
        send_package(self.chatter, header)
        message_lock.release()
        self.chatter_recv = ReceiveMessageThread(self.chatter)
        self.chatter_recv.msg_pack.connect(self.show_message)
        self.chatter_recv.start()

        self.portrait_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.portrait_client.connect(RESOURCE_SERVER_ADDRESS)
        self._fetch_others_portrait(self.id)

    def _flush(self):
        """
        刷新用户信息
        每次设置成功后调用
        :return:
        """
        self.userSettings = SettingsGui(self.id, self.userName, self.favComic, self.isKnow)
        self.label_username.setText(self.userName)
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")

    def show_biography(self, user_id, x, y):
        print(f"{user_id} {x} {y}")
        self.biography = Biography(user_id, x, y, PORTRAIT_PATH, self.db_conn, TABLE_NAME)
        self.biography.show()

    def system_information(self, system_code):
        if system_code == 'KICK OUT':
            # 将close 与kickout 信号连接
            self.dialog = Dialog('KICK OUT')
            self.dialog.close_signal.connect(self.close)
            # 弹出提示框
            self.dialog.show()
        if system_code == 'LOGIN REPEAT':
            # 弹出提示框
            self.dialog = Dialog('LOGIN REPEAT')
            self.dialog.show()


    def show_message(self, msg_pack):
        """
        展示信息
        :return:
        """
        if 'system_code' in msg_pack:
            self.system_information(msg_pack['system_code'])
        time_ = msg_pack['time']
        user_id = msg_pack['user_id']
        user_name = msg_pack['user_name']
        widget = QWidget()
        layout_main = QHBoxLayout()
        layout_msg = QVBoxLayout()
        portrait = Portrait(int(user_id))
        portrait.connect_customized_slot(self._fetch_others_portrait)
        portrait.connect_pos_slot(self.show_biography)
        portrait.setFixedSize(50, 50)
        img = QPixmap(PORTRAIT_PATH % user_id).scaled(50, 50)
        portrait.setPixmap(img)
        layout_msg.addWidget(QLabel(f'{time_}  {user_name}'))
        item = QListWidgetItem()
        if 'image' in msg_pack:
            shape = msg_pack['shape']
            image_np = np.frombuffer(msg_pack['image'], dtype='uint8').reshape(shape)
            image = Image.fromarray(image_np).convert('RGB')
            pixmap = image.toqpixmap().scaled(200,200)
            image_label = QLabel()
            image_label.setFixedSize(400,200)
            image_label.setPixmap(pixmap)
            layout_msg.addWidget(image_label)
            item.setSizeHint(QSize(400, 250))
        else:
            msg = msg_pack['message']
            msg_list = split_message(msg)
            for msg_splited in msg_list:
                layout_msg.addWidget(QLabel(msg_splited))
            item.setSizeHint(QSize(200, 70 + (len(msg_list) - 1) * 35))
        if self.id == user_id:
            layout_main.addLayout(layout_msg)
            layout_main.addWidget(portrait)
        else:
            layout_main.addWidget(portrait)
            layout_main.addLayout(layout_msg)
        widget.setLayout(layout_main)


        self.msg_list.addItem(item)
        self.msg_list.setItemWidget(item, widget)
        self.msg_list.scrollToBottom()

    def send_message(self):
        """
        发送消息
        :return:
        """
        # msg = self.textEdit.toHtml()
        msg = self.textEdit.toPlainText()
        if msg == '':
            self.message_empty_info()
            return
        self.textEdit.clear()
        pack = {
            'user_id': self.id,
            'user_name': self.userName,
            'message': msg
        }
        message_lock.acquire()
        send_package(self.chatter, pack)
        message_lock.release()

    def message_empty_info(self):
        """
        空信息提示
        :return:
        """
        empty_info = QLabel(self)
        empty_info.setText('不能发送空信息')
        empty_info.setGeometry(QRect(420, 160, 131, 20))
        empty_info.setAlignment(Qt.AlignCenter)
        empty_info.show()
        threading.Thread(target=self._close_label, args=(empty_info,)).start()

    def _close_label(self, label):
        """
        多线程提示（等待一秒）
        :param label:
        :return:
        """
        sleep(1)
        label.close()

    def user_setting(self):
        """
        打开设置界面
        :return:
        """
        self.userSettings.flush()
        self.userSettings.show()
        self.userSettings._signal.connect(self._update)

    def _send_portrait(self):
        header = {
            'type': 'send',
            'user_id': self.id,
            'file_size': os.path.getsize(self.portrait)
        }
        print('发送头像', header)
        send_package(self.portrait_client, header)
        with open(self.portrait, 'rb') as f:
            for line in f:
                self.portrait_client.send(line)
        print('发送成功')

    def _update(self, params):
        """
        更新用户信息
        :param params:
        :return:
        """
        self.userName = params['user_name']
        self.favComic = params['fac_comic']
        self.isKnow = params['is_know']
        self.db_conn.edit(TABLE_NAME, [self.id, 'name', self.userName])
        self.db_conn.edit(TABLE_NAME, [self.id, 'anime', self.favComic])
        self._flush()
        threading.Thread(target=self._send_portrait).start()

    def send_emoji(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('你在肝肾莫')
        dialog.resize(400,400)
        label = QLabel("不会真有人以为我实现了这个功能吧^^_", dialog)
        label.setGeometry(QRect(50,50,300,300))
        dialog.show()

    def send_image(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件", './',
                                                           "图片文件 (*.jpg);;图片文件 (*.png)")
        if file_type == '' and file_name == '':
            return
        image = Image.open(file_name)
        image_np = np.array(image)
        pack = {
            'user_id': self.id,
            'user_name': self.userName,
            'shape': image_np.shape,
            'image': image_np.tostring()
        }
        message_lock.acquire()
        print(f'开始发送图片包')
        send_package(self.chatter, pack)
        message_lock.release()
        print('发送成功')


    def send_file(self):
        self.send_emoji()

    def eventFilter(self, obj, event):
        """
        事件过滤器
        :param obj:
        :param event:
        :return:
        """
        if obj is self.textEdit:  # 按下回车发送
            if event.type() == QEvent.KeyPress and (
                    event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
                self.send_message()
                return True  # 表示过滤此事件

        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    id = 4
    user_name = '牛蛙丶丶'
    fav_comic = 'Attack on Titan'
    is_know = True
    gui = ChatGUI(id, user_name, fav_comic, is_know)
    gui.show()
    sys.exit(app.exec_())
