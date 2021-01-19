import sys
from time import sleep, strftime, localtime
import threading

from PyQt5.QtGui import QPixmap, QIcon, QTextCursor
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget

from VChat import Ui_Form
from SettingsGui import SettingsGui

def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class ChatGUI(QWidget,Ui_Form):

    def __init__(self, user_name, portrait, fav_comic, is_know):
        super(ChatGUI, self).__init__()
        self.setupUi(self)

        self.userName = user_name
        self.portrait = portrait
        self.favComic = fav_comic
        self.isKnow = is_know
        self.userSettings = SettingsGui(self.userName, self.portrait, self.favComic, self.isKnow)

        self.label_username.setText(self.userName)
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")

        self.textEdit_msg_box.setReadOnly(True)
        self.textEdit.installEventFilter(self)

    def send_message(self):
        """
        发送消息
        :return:
        """
        msg = self.textEdit.toPlainText()
        if msg == '':
            self.message_empty_info()
            return
        self.textEdit.clear()
        self.textEdit_msg_box.append(get_localtime())
        self.textEdit_msg_box.append(f'<img src="{self.portrait}" id="portrait" width="50"/>{self.userName}: ' + msg)
        self.textEdit_msg_box.append('')
        self.textEdit_msg_box.moveCursor(self.textEdit_msg_box.textCursor().End)

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
        sleep(1)
        label.close()

    def user_setting(self):
        self.userSettings.show()

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


class Child(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我是子窗口啊")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    user_name = 's6第一个王者'
    portrait = './resource/Saten_Ruiko.jpg'
    fav_comic = 'Attack on Titan'
    is_know = True
    gui = ChatGUI(user_name, portrait, fav_comic, is_know)
    gui.show()
    sys.exit(app.exec_())