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
from gui.EmojiWindow import EmojiWindow
from gui.ChatWidget import *
from authentication.constantName import *
from authentication.dialogGUI import *

SERVER_IP = '39.106.169.58'
SERVER_ADDRESS = ('39.106.169.58', 3976)
VIDEO_SERVER_ADDRESS = ('39.106.169.58', 3977)
AUDIO_SERVER_ADDRESS = ('39.106.169.58', 3978)
RESOURCE_SERVER_ADDRESS = ('39.106.169.58', 3979)
LINE_LENGTH = 39
UNI2ASC = 40 / 24
message_lock = threading.Lock()


def split_message(msg):
    msg_list = []
    size = 0
    now = ''
    for char in msg:
        size += 1 if ord(char) < 128 else UNI2ASC
        now += char
        if size > LINE_LENGTH:
            msg_list.append(now)
            size = 0
            now = ''
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


class ReceiveMessageThread(QThread):
    msg_pack = pyqtSignal(dict)

    def __init__(self, chatter):
        super().__init__()
        self.chatter = chatter

    def run(self):
        while True:
            try:
                pack = fetch_package(self.chatter)
                print(pack)
                self.msg_pack.emit(pack)
                sleep(0.1)
            except Exception as e:
                print('Receiver Message Error', e)
                break


class ChatGUI(QWidget, Ui_Form):

    def __init__(self, user_id, user_name, fav_comic, profile, db_conn):
        super(ChatGUI, self).__init__()
        self.setupUi(self)

        icon = QIcon()
        icon.addPixmap(QPixmap("../gui/resource/shaco_logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.emoji_button.setIcon(QIcon("../gui/resource/button/emoji_button.png"))
        self.emoji_button.setIconSize(QSize(39, 28))
        self.image_button.setIcon(QIcon("../gui/resource/button/image_button.png"))
        self.image_button.setIconSize(QSize(39, 28))
        self.file_button.setIcon(QIcon("../gui/resource/button/file_button.png"))
        self.file_button.setIconSize(QSize(39, 28))
        self.notice_label.setPixmap(QPixmap('../gui/resource/label/friend_list.png'))
        self.notice_label.setScaledContents(True)
        self.notice_label.clicked_signal.connect(self.show_process)
        self.id = user_id
        self.userName = user_name
        self.portrait = f'../gui/resource/portrait/{self.id}.jpg'
        self.favComic = fav_comic
        self.profile = profile
        self._flush()

        self.db_conn = db_conn

        self.init_client()

        self.textEdit.setStyleSheet("font:20px")
        self.textEdit.installEventFilter(self)

        # 初始化登出或登录通知
        self.dialog = None
        # 初始化个人简介页面
        self.biography = None
        # 初始化好友请求
        self.apply_friend_window = None
        # 初始化好友请求结果
        self.result_apply_friend_window = None
        # 初始化好友处理界面
        self.friend_process_window = None
        # 待办事项
        self.to_do_list = []
        # 立即处理的system_code
        self.system_code_instant = [SYSTEM_CODE_KICK_OUT,
                                    SYSTEM_CODE_LOGIN_REPEAT,
                                    SYSTEM_CODE_REPEAT_FRIEND_APPLY]

        self.emoji_window = EmojiWindow()
        self.emoji_window.connect_slot(self.insert_emoji)

        self.tabWidget.tabBar().hide()
        self.create_tab()
        self.cur_user_id = None
        self.add_friend()
        self.user2tab = {}
        self.load_friends()

    def load_friends(self):
        friends = self.db_conn.search(TABLE_NAME_FRIENDINFO, ['id', self.id])
        if friends is None:
            return
        for friend_id in friends:
            friend_name = self.db_conn.search(TABLE_NAME_USERINFO, ['id', friend_id])[0][1]
            self.add_friend(friend_id, friend_name, new=False)

    def delete_friend(self, friend_id):
        for index in range(self.frineds_list.count()):
            item = self.frineds_list.item(index)
            widget = self.frineds_list.itemWidget(item)
            if widget.user_id == friend_id:
                self.frineds_list.takeItem(index)
                del item
                break
        if friend_id in self.user2tab:
            del self.user2tab[friend_id]
        if self.cur_user_id == friend_id:
            self.switch_tab()

    def add_friend(self, friend_id=None, friend_name=None, new=True):
        print('add friend', friend_id, friend_name)
        if friend_id is not None and new is True:
            self.db_conn.insert(TABLE_NAME_FRIENDINFO, [self.id, friend_id])
        item = QListWidgetItem()
        if friend_id is None:
            widget = BiographyWidget(friend_id, self.switch_tab)
        else:
            widget = BiographyWidget(friend_id, self._fetch_others_portrait, self.show_biography)
        layout = QHBoxLayout()
        if friend_id is None:
            friend_name = "ShacoRoom"
            img = QPixmap('resources/pic/shaco.jpg').scaled(30, 30)
        else:
            portrait_path = PORTRAIT_PATH % friend_id
            img = QPixmap(portrait_path).scaled(30, 30)
        portrait = QLabel()
        portrait.setPixmap(img)
        layout.addWidget(portrait)
        layout.addWidget(QLabel(friend_name))
        layout.setStretch(3, 7)
        widget.setLayout(layout)
        item.setSizeHint(QSize(150, 55))
        self.frineds_list.addItem(item)
        self.frineds_list.setItemWidget(item, widget)

    def switch_tab(self, user_id=None):
        print('swith', user_id)
        if user_id is None:
            self.tabWidget.setCurrentIndex(0)
        elif user_id not in self.user2tab:
            self.create_tab(user_id)
            self.tabWidget.setCurrentIndex(self.user2tab[user_id][1])
        else:
            self.tabWidget.setCurrentIndex(self.user2tab[user_id][1])
        self.cur_user_id = user_id

    def create_tab(self, user_id=None):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        list_widget = QListWidget()
        layout.addWidget(list_widget)
        if user_id is None:
            self.shaco_tab.setLayout(layout)
            self.shaco_tab = list_widget
        else:
            widget = QWidget()
            widget.setLayout(layout)
            self.tabWidget.addTab(widget, '')
            self.user2tab[user_id] = (list_widget, self.tabWidget.count() - 1)

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
        self.userSettings = SettingsGui(self.id, self.userName, self.favComic, self.profile)
        self.label_username.setText(self.userName)
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")

    def show_biography(self, target_id, x, y):
        print(f"{target_id} {x} {y}")
        self.biography = Biography(self.id, self.userName, target_id, x, y,
                                   self.db_conn, self.chatter, self.switch_tab, self.delete_friend)
        self.biography.show()

    def show_process(self):
        print(self.to_do_list)
        self.friend_process_window = FriendProcess(self.to_do_list, self.system_information,
                                                   self.delete_todolist)
        self.friend_process_window.show()

    def delete_todolist(self, target_index):
        del self.to_do_list[target_index]
        print(self.to_do_list)
        if not self.to_do_list:
            self.notice_label.setPixmap(QPixmap('../gui/resource/label/friend_list.png'))


    def insert_emoji(self, emo):
        self.textEdit.insertPlainText(emo)

    def system_information(self, pack):
        if pack['system_code'] == SYSTEM_CODE_KICK_OUT:
            # 将close 与kickout 信号连接
            self.dialog = Dialog(SYSTEM_CODE_KICK_OUT)
            self.dialog.close_signal.connect(self.close)
            # 弹出提示框
            self.dialog.show()
        if pack['system_code'] == SYSTEM_CODE_LOGIN_REPEAT:
            # 弹出提示框
            self.dialog = Dialog(SYSTEM_CODE_LOGIN_REPEAT)
            self.dialog.show()
        if pack['system_code'] == SYSTEM_CODE_FRIEND_APPLY:
            self.apply_friend_window = FriendApply(self.id, pack['send_id'], pack['send_name'],
                                                   pack['message'], self.chatter)
            self.apply_friend_window.accept_signal.connect(self.add_friend)
            self.apply_friend_window.show()
        if pack['system_code'] == SYSTEM_CODE_RESULT_FRIEND_APPLY:
            # 好友请求的结果
            self.result_apply_friend_window = ResultFriendApply(self.id, pack['send_id'], pack['send_name'],
                                                                pack['message'], PORTRAIT_PATH)
            if pack['message'] == 'ACCEPT':
                self.add_friend(pack['send_id'], pack['send_name'])
            self.result_apply_friend_window.show()

        if pack['system_code'] == SYSTEM_CODE_REPEAT_FRIEND_APPLY:
            self.result_apply_friend_window = ResultFriendApply(self.id, pack['send_id'], pack['send_name'],
                                                                pack['message'], PORTRAIT_PATH)
            self.result_apply_friend_window.show()

        if pack['system_code'] == SYSTEM_CODE_RESULT_DELETE_FRIEND:
            # 删除好友
            self.result_apply_friend_window = ResultFriendApply(self.id, pack['send_id'], pack['send_name'],
                                                                pack['message'], PORTRAIT_PATH)
            self.delete_friend(pack['send_id'])
            self.result_apply_friend_window.show()

    def add_to_do_list(self, pack):
        result = self.db_conn.search(TABLE_NAME_USERINFO, ['id', pack['send_id']])
        dict_to_add = {'self_id': self.id, 'send_id': pack['send_id'], 'send_name': result[0][1],
                       'message': pack['message'], 'system_code': pack['system_code']}
        print(dict_to_add)
        if dict_to_add['system_code'] in self.system_code_instant:
            # 重复登陆或强制下线立即执行而不是加入到to_do_list
            self.system_information(dict_to_add)
        else:
            self.to_do_list.append(dict_to_add)
            # 更改通知图标为带红点的
            self.notice_label.setPixmap(QPixmap('../gui/resource/label/friend_list_red.png'))
            self.notice_label.setScaledContents(True)

    def show_message(self, msg_pack):
        """
        展示信息
        :return:
        """
        if 'system_code' in msg_pack:
            self.add_to_do_list(msg_pack)
            return
        time_ = msg_pack['time']
        user_id = msg_pack['user_id']
        user_name = msg_pack['user_name']
        widget = QWidget()
        layout_main = QHBoxLayout()
        layout_msg = QVBoxLayout()
        portrait = BiographyLabel(int(user_id), self._fetch_others_portrait, self.show_biography)
        portrait.setFixedSize(50, 50)
        img = QPixmap(PORTRAIT_PATH % user_id).scaled(50, 50)
        portrait.setPixmap(img)
        head = QLabel(f'{time_}  {user_name}')
        head.setFont(QFont("Microsoft YaHei"))
        head.setStyleSheet("font: bold")
        layout_msg.addWidget(head)
        item = QListWidgetItem()
        if 'image' in msg_pack:
            shape = msg_pack['shape']
            image_np = np.frombuffer(msg_pack['image'], dtype='uint8').reshape(shape)
            image = Image.fromarray(image_np).convert('RGB')
            pixmap = image.toqpixmap().scaled(200, 200)
            image_label = QLabel()
            image_label.setFixedSize(500, 200)
            image_label.setPixmap(pixmap)
            layout_msg.addWidget(image_label)
            item.setSizeHint(QSize(500, 250))
        else:
            msg = msg_pack['message']
            msg_list = split_message(msg)
            for msg_splited in msg_list:
                layout_msg.addWidget(QLabel(msg_splited))
            item.setSizeHint(QSize(500, 70 + (len(msg_list) - 1) * 35))
        if self.id == user_id:
            layout_main.addLayout(layout_msg)
            layout_main.addWidget(portrait)
        else:
            layout_main.addWidget(portrait)
            layout_main.addLayout(layout_msg)
        widget.setLayout(layout_main)

        if 'to_id' in msg_pack:
            other_id = user_id if user_id != self.id else msg_pack['to_id']
            if other_id not in self.user2tab:
                self.create_tab(other_id)
            self.user2tab[other_id][0].addItem(item)
            self.user2tab[other_id][0].setItemWidget(item, widget)
            self.user2tab[other_id][0].scrollToBottom()
        else:
            self.shaco_tab.addItem(item)
            self.shaco_tab.setItemWidget(item, widget)
            self.shaco_tab.scrollToBottom()

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
        if self.cur_user_id is not None:
            pack['to_id'] = self.cur_user_id
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
        self.favComic = params['fav_comic']
        self.profile = params['profile']
        self.db_conn.edit(TABLE_NAME_USERINFO, [self.id, 'name', self.userName])
        self.db_conn.edit(TABLE_NAME_USERINFO, [self.id, 'anime', self.favComic])
        self.db_conn.edit(TABLE_NAME_USERINFO, [self.id, 'profile', self.profile])
        self._flush()
        threading.Thread(target=self._send_portrait).start()

    def send_emoji(self):
        pos = self.emoji_button.mapToGlobal(self.emoji_button.pos())
        self.emoji_window.move(pos.x(), pos.y() - 200)
        self.emoji_window.show()

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
        send_package(self.chatter, pack)
        message_lock.release()

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
