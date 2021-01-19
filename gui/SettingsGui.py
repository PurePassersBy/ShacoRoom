import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication

from VSettings import Ui_Dialog


class SettingsGui(QWidget, Ui_Dialog):
    _signal = QtCore.pyqtSignal(dict)
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

    def flush(self):
        self.graphicsView.setStyleSheet(f"border-image: url({self.portrait});")
        self.lineEdit_username.setText(self.userName)
        self.lineEdit_fav_comic.setText(self.favComic)
        if self.isKnow:
            self.checkBox_yes.setCheckState(QtCore.Qt.Checked)

    def accept(self):
        dic = dict()
        dic['user_name'] = self.lineEdit_username.text()
        dic['fac_comic'] = self.lineEdit_fav_comic.text()
        dic['is_know'] = bool(self.checkBox_yes.checkState())
        self._signal.emit(dic)

    def reject(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_name = 's6第一个王者'
    portrait = './resource/Saten_Ruiko.jpg'
    fav_comic = 'Attack on Titan'
    is_know = True
    setting = SettingsGui(user_name, portrait, fav_comic, is_know)
    setting.show()
    sys.exit(app.exec_())