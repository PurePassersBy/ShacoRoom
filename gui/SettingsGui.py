import sys
import shutil

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtGui import *

from gui.VSettings import Ui_Dialog


class SettingsGui(QWidget, Ui_Dialog):
    _signal = QtCore.pyqtSignal(dict)
    def __init__(self, user_id, user_name, fav_comic, profile):
        super(SettingsGui, self).__init__()
        self.setupUi(self)
        self.id = user_id
        self.userName = user_name
        self.portrait = f'../gui/resource/portrait/{self.id}.jpg'
        self.favComic = fav_comic
        self.profile = profile

        icon = QIcon()
        icon.addPixmap(QPixmap("../gui/resource/shaco_logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")
        self.lineEdit_username.setText(self.userName)
        self.lineEdit_fav_comic.setText(self.favComic)
        self.textEdit.setText(self.profile)

    def load_file(self):
        """
        加载头像图片
        :return:
        """
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件", './',
                                                           "图片文件 (*.jpg);;图片文件 (*.png)")
        if file_type == '' and file_name == '':
            return
        file_type = file_type[-4:-1]
        shutil.copyfile(file_name, f'../gui/resource/portrait/{self.id}.{file_type}') # 唯一标识符命名存储头像

    def flush(self):
        """
        刷新个人信息
        :return:
        """
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")
        self.lineEdit_username.setText(self.userName)
        self.lineEdit_fav_comic.setText(self.favComic)
        self.textEdit.setText(self.profile)


    def accept(self):
        """
        成功修改个人设置
        :return:
        """
        dic = dict()
        dic['user_name'] = self.lineEdit_username.text()
        dic['fav_comic'] = self.lineEdit_fav_comic.text()
        dic['profile'] = self.textEdit.toPlainText()
        self._signal.emit(dic)

    def reject(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id = 0
    user_name = 's6第一个王者'
    fav_comic = 'Attack on Titan'
    profile = '寄！'
    setting = SettingsGui(user_id, user_name, fav_comic, profile)
    setting.show()
    sys.exit(app.exec_())