import sys
import os
import json
import struct
from time import sleep
import threading
import socket

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

sys.path.append('..')
from gui.VChat import Ui_Form
from gui.SettingsGui import SettingsGui
from authentication.dialogGUI import Dialog

SERVER_IP = '39.106.169.58'
SERVER_ADDRESS = ('39.106.169.58', 3976)
VIDEO_SERVER_ADDRESS = ('39.106.169.58', 3977)
AUDIO_SERVER_ADDRESS = ('39.106.169.58', 3978)
RESOURCE_SERVER_ADDRESS = ('39.106.169.58', 3979)
PORTRAIT_PATH = '../gui/resource/portrait/%s.jpg'
TABLE_NAME = 'userinfo'


def send_package(conn, pack):
    pack_str = json.dumps(pack).encode()
    conn.send(struct.pack('i', len(pack_str)))
    conn.send(pack_str)


def fetch_package(conn):
    size = struct.unpack('i', conn.recv(4))[0]
    pack = json.loads(conn.recv(size).decode())
    return pack


class Portrait(QLabel):
    clicked_signal = pyqtSignal(int)

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id

    def mousePressEvent(self, QMouseEvent):
        self.clicked_signal.emit(self.user_id)

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

    def _fetch_others_portrait(self, user_id):
        query = {
            'type': 'fetch',
            'user_id': user_id
        }
        send_package(self.portrait_client, query)
        header = fetch_package(self.portrait_client)
        file_size = header['file_size']
        if file_size == 0:
            return
        file_path = f'../gui/resource/portrait/{user_id}.jpg'
        with open(file_path, 'wb') as f:
            recv_size = 0
            while recv_size < file_size:
                data = self.portrait_client.recv(1024)
                f.write(data)
                recv_size += len(data)

    def init_client(self):
        self.chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatter.connect(SERVER_ADDRESS)
        header = {
            'user_id': self.id,
            'user_name': self.userName
        }
        send_package(self.chatter, header)
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

    def system_information(self, system_code):
        print('sdfssdf')
        if system_code == 'KICK OUT':
            # 将close 与kickout 信号连接
            print('???')
            self.dialog = Dialog('KICK OUT')
            self.dialog.close_signal.connect(self.close)
            print('connect signal')
            # 发送下线成功的响应给服务器
            # kickout_package = {
            #     'user_id': self.id,
            #     'user_name': self.userName,
            #     'message': '该账号在其他客户端登录，您已被强制下线',
            #     'system_code': 'SUCCESS'}
            # pack_str = json.dumps(kickout_package).encode()
            # print('Sending Kick out request to server')
            # self.chatter.send(struct.pack('i', len(pack_str)))
            # self.chatter.send(pack_str)
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
        print(msg_pack)
        if 'system_code' in msg_pack.keys():
            self.system_information(msg_pack['system_code'])
        print('out')
        time_ = msg_pack['time']
        user_id = msg_pack['user_id']
        user_name = msg_pack['user_name']
        msg = msg_pack['message']
        widget = QWidget()
        layout_main = QHBoxLayout()
        layout_msg = QVBoxLayout()
        portrait = Portrait(int(user_id))
        portrait.connect_customized_slot(self._fetch_others_portrait)
        portrait.setFixedSize(50, 50)
        img = QPixmap(PORTRAIT_PATH % user_id).scaled(50, 50)
        portrait.setPixmap(img)
        layout_msg.addWidget(QLabel(f'{time_}  {user_name}'))
        layout_msg.addWidget(QLabel(msg))
        if self.id == user_id:
            layout_main.addLayout(layout_msg)
            layout_main.addWidget(portrait)
        else:
            layout_main.addWidget(portrait)
            layout_main.addLayout(layout_msg)
        widget.setLayout(layout_main)
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 70))
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
        send_package(self.chatter, pack)

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
        send_package(self.portrait_client, header)
        with open(self.portrait, 'rb') as f:
            for line in f:
                self.portrait_client.send(line)

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
        self._flush()
        threading.Thread(target=self._send_portrait).start()

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
