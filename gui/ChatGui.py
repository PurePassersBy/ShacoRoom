import sys
from time import sleep, strftime, localtime
import threading
import socket

from PyQt5.QtGui import QPixmap, QIcon, QTextCursor
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget

from VChat import Ui_Form
from SettingsGui import SettingsGui

SERVER_ADDRESS = ('39.106.169.58', 3976)
VIDEO_SERVER_ADDRESS = ('39.106.169.58', 3977)
AUDIO_SERVER_ADDRESS = ('39.106.169.58', 3978)


class ChatGUI(QWidget,Ui_Form):

    def __init__(self, user_name, portrait, fav_comic, is_know):
        super(ChatGUI, self).__init__()
        self.setupUi(self)

        self.userName = user_name
        self.portrait = portrait
        self.favComic = fav_comic
        self.isKnow = is_know
        self._flush()

        self.init_chatter()

        self.textEdit_msg_box.setReadOnly(True)
        self.textEdit.installEventFilter(self)

    def init_chatter(self):
        self.chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatter.connect(SERVER_ADDRESS)
        self.chatter.send(self.userName.encode())
        receiver = threading.Thread(target=self.recv_message)
        receiver.setDaemon(True)
        receiver.start()

    def _flush(self):
        """
        刷新用户信息
        每次设置成功后调用
        :return:
        """
        self.userSettings = SettingsGui(self.userName, self.portrait, self.favComic, self.isKnow)
        self.label_username.setText(self.userName)
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")

    def recv_message(self):
        """
        接收消息
        :return:
        """
        while True:
            try:
                msg = self.chatter.recv(1024).decode()
                msg_ls = msg.split(' ')
                ltime = ' '.join(msg_ls[:2])
                user_name = msg_ls[2]
                msg = ' '.join(msg_ls[3:])
                msg = '<div id="self">' + msg + '</div>'
                self.textEdit_msg_box.append(ltime)
                self.textEdit_msg_box.append(
                    f'<img src="{self.portrait}" id="portrait" width=50 height=50/>{user_name}: ' + msg)
                self.textEdit_msg_box.append('')
                self.textEdit_msg_box.moveCursor(self.textEdit_msg_box.textCursor().End)

                print(self.textEdit_msg_box.toHtml())
            except Exception as e:
                print(e)
                break

    def send_message(self):
        """
        发送消息
        :return:
        """
        msg = self.textEdit.toHtml()
        # print(msg)
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
        empty_info.setGeometry(QtCore.QRect(420, 160, 131, 20))
        empty_info.setAlignment(QtCore.Qt.AlignCenter)
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

    def _update(self, params):
        """
        更新用户信息
        :param params:
        :return:
        """
        self.userName = params['user_name']
        self.favComic = params['fac_comic']
        self.isKnow = params['is_know']
        self._flush()

        # TODO: 在服务端同步更新
        # TODO: 头像的更新

    def eventFilter(self, obj, event):
        """
        事件过滤器
        :param obj:
        :param event:
        :return:
        """
        if obj is self.textEdit:  # 按下回车发送
            if event.type() == QtCore.QEvent.KeyPress and (
                    event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return):
                self.send_message()
                return True  # 表示过滤此事件

        return False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    user_name = '牛蛙丶丶'
    portrait = './resource/Saten_Ruiko.jpg'
    fav_comic = 'Attack on Titan'
    is_know = True
    gui = ChatGUI(user_name, portrait, fav_comic, is_know)
    gui.show()
    sys.exit(app.exec_())