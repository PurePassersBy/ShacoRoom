import sys
import shutil

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

from gui.VSettings import Ui_Dialog


class SettingsGui(QWidget, Ui_Dialog):
    _signal = QtCore.pyqtSignal(dict)
    def __init__(self, user_id, user_name, fav_comic, is_know):
        super(SettingsGui, self).__init__()
        self.setupUi(self)
        self.id = user_id
        self.userName = user_name
        self.portrait = f'./resource/portrait/{self.id}.jpg'
        self.favComic = fav_comic
        self.isKnow = is_know

        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")
        self.lineEdit_username.setText(self.userName)
        self.lineEdit_fav_comic.setText(self.favComic)
        if self.isKnow:
            self.checkBox_yes.setCheckState(QtCore.Qt.Checked)

    def load_file(self):
        """
        加载头像图片
        :return:
        """
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件", './',
                                                           "图片文件 (*.jpg);;图片文件 (*.png)")
        file_type = file_type[-4:-1]
        shutil.copyfile(file_name, f'./resource/portrait/{self.id}.{file_type}') # 唯一标识符命名存储头像

    def flush(self):
        """
        刷新个人信息
        :return:
        """
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")
        self.lineEdit_username.setText(self.userName)
        self.lineEdit_fav_comic.setText(self.favComic)
        if self.isKnow:
            self.checkBox_yes.setCheckState(QtCore.Qt.Checked)

    def accept(self):
        """
        成功修改个人设置
        :return:
        """
        dic = dict()
        dic['user_name'] = self.lineEdit_username.text()
        dic['fac_comic'] = self.lineEdit_fav_comic.text()
        dic['is_know'] = bool(self.checkBox_yes.checkState())
        self._signal.emit(dic)

    def reject(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id = 0
    user_name = 's6第一个王者'
    fav_comic = 'Attack on Titan'
    is_know = True
    setting = SettingsGui(user_id, user_name, fav_comic, is_know)
    setting.show()
    sys.exit(app.exec_())