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

from gui.VChat import Ui_Form
from gui.SettingsGui import SettingsGui

SERVER_IP = '39.106.169.58'
SERVER_ADDRESS = ('39.106.169.58', 3976)
VIDEO_SERVER_ADDRESS = ('39.106.169.58', 3977)
AUDIO_SERVER_ADDRESS = ('39.106.169.58', 3978)
RESOURCE_SERVER_ADDRESS = ('39.106.169.58', 3979)
PORTRAIT_PATH = '../gui/resource/portrait/%s.jpg'
TABLE_NAME = 'userinfo'

class ReceiveMessageThread(QThread):
    msg_pack = pyqtSignal(dict)
    def __init__(self, chatter):
        super().__init__()
        self.chatter = chatter

    def run(self):
        while True:
            try:
                msg = self.chatter.recv(1024).decode()
                msg_ls = msg.split(' ')
                ltime = ' '.join(msg_ls[:2])
                user_id = msg_ls[2]
                msg = ' '.join(msg_ls[3:])
                print(ltime)
                pack = {
                    'time':ltime,
                    'user_id':user_id,
                    'message':msg
                }
                self.msg_pack.emit(pack)
                sleep(0.1)
            except Exception as e:
                print('recv msg', e)
                break

class ChatGUI(QWidget,Ui_Form):

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
        #self.get_others_info()

        self.textEdit.installEventFilter(self)
        print('done')

    def _get_others_portrait(self):
        while True:
            try:
                header_size = struct.unpack('i', self.portrait_client.recv(4))[0]
                header_str = self.portrait_client.recv(header_size)
                header = json.loads(header_str.decode())
                user_id = header['user_id']
                file_size = header['file_size']
                file_path = f'../gui/resource/{user_id}.jpg'
                with open(file_path, 'wb') as f:
                    recv_size = 0
                    while recv_size < file_size:
                        data = self.portrait_client.recv(1024)
                        f.write(data)
                        recv_size += len(data)
            except Exception as e:
                print('get portrait error', e)
                break



    def get_others_info(self):
        threading.Thread(target=(self._get_others_portrait)).start()


    def init_client(self):
        self.chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatter.connect(SERVER_ADDRESS)
        self.chatter.send(str(self.id).encode())
        self.chatter_recv = ReceiveMessageThread(self.chatter)
        self.chatter_recv.msg_pack.connect(self.show_message)
        self.chatter_recv.start()

        self.portrait_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.portrait_client.connect(RESOURCE_SERVER_ADDRESS)

    def _flush(self):
        """
        刷新用户信息
        每次设置成功后调用
        :return:
        """
        self.userSettings = SettingsGui(self.id, self.userName, self.favComic, self.isKnow)
        self.label_username.setText(self.userName)
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")

    def show_message(self, msg_pack):
        """
        展示信息
        :return:
        """
        time_ = msg_pack['time']
        user_id = msg_pack['user_id']
        user_name = self.db_conn.search('userinfo', ['id', user_id])[0][1]
        msg = msg_pack['message']
        widget = QWidget()
        layout_main = QHBoxLayout()
        layout_msg = QVBoxLayout()
        portrait = QLabel()
        portrait.setFixedSize(50,50)
        img = QPixmap(PORTRAIT_PATH%user_id).scaled(50,50)
        portrait.setPixmap(img)
        layout_msg.addWidget(QLabel(f'{time_}  {user_name}'))
        layout_msg.addWidget(QLabel(msg))
        if str(self.id) == user_id:
            layout_main.addLayout(layout_msg)
            layout_main.addWidget(portrait)
        else:
            layout_main.addWidget(portrait)
            layout_main.addLayout(layout_msg)
        widget.setLayout(layout_main)
        item = QListWidgetItem()
        item.setSizeHint(QSize(200,70))
        self.msg_list.addItem(item)
        self.msg_list.setItemWidget(item, widget)
        self.msg_list.scrollToBottom()

    def send_message(self):
        """
        发送消息
        :return:
        """
        #msg = self.textEdit.toHtml()
        msg = self.textEdit.toPlainText()
        if msg == '':
            self.message_empty_info()
            return
        self.textEdit.clear()
        self.chatter.send(msg.encode())

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
        print('send portrait...')
        #client = socket.socket()
        #client.connect(RESOURCE_SERVER_ADDRESS)
        header = {
            'user_id': self.id,
            'file_size': os.path.getsize(self.portrait)
        }
        header_str = json.dumps(header).encode()
        self.portrait_client.send(struct.pack('i', len(header_str)))
        self.portrait_client.send(header_str)
        with open(self.portrait, 'rb') as f:
            for line in f:
                self.portrait_client.send(line)
        # client.close()
        print('send done')

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