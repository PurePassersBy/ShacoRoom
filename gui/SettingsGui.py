import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication

from VSettings import Ui_Dialog


class SettingsGui(QWidget, Ui_Dialog):
    def __init__(self, user_name, portrait, fav_comic, is_know):
        super(SettingsGui, self).__init__()
        self.setupUi(self)
        self.userName = user_name
        self.portrait = portrait
        self.favComic = fav_comic
        self.isKnow = is_know

        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")
        self.lineEdit_username.setText(self.userName)
        self.lineEdit_fav_comic.setText(self.favComic)
        if self.isKnow:
            self.checkBox_yes.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_no.setCheckState(QtCore.Qt.Checked)

    def accept(self):
        pass

    def reject(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_name = 's6第一个王者'
    portrait = './resource/Saten_Ruiko.jpg'
    fav_comic = 'Attack on Titan'
    is_know = True
    setting = SettingsGui(user_name, portrait, fav_comic, is_know)
    setting.show()
    sys.exit(app.exec_())