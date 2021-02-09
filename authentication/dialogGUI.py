# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.setMaximumSize(QtCore.QSize(400, 300))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 60, 291, 91))
        font = QtGui.QFont()
        font.setFamily("Italic")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 130, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Italic")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "注册成功！赶快加入马戏团"))
        self.label_2.setText(_translate("Dialog", "和沙口们一起来场马戏的盛宴吧！"))

class Dialog(QMainWindow, Ui_Dialog):
    # pyqtSignal 要定义为一个类而不是属性，不能放到__init__里
    close_signal = QtCore.pyqtSignal()

    def __init__(self, infomation):
        """
        注意close_signal 要在类成员函数外定义
        初始化CloseDialog类，将 确定 和 取消 按钮连接到self._close函数
        :param
        :return:
        """
        super(Dialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self._close)
        self.buttonBox.rejected.connect(self._close)
        self.type = infomation
        self._set_text()
    def _set_text(self):
        _translate = QtCore.QCoreApplication.translate
        if self.type == 'REGISTER SUCCESS':
            self.label.setText(_translate("Dialog", "注册成功！赶快加入马戏团"))
            self.label_2.setText(_translate("Dialog", "和沙口们一起来场马戏的盛宴吧！"))
        if self.type =='EDIT SUCCESS':
            self.label.setText(_translate("Dialog", "密码修改成功！"))
            self.label_2.setText(_translate("Dialog", "注意保管好密码哦"))
        if self.type == 'LOGIN REPEAT':
            self.label.setText(_translate("Dialog", "该账户已登录"))
            self.label_2.setText(_translate("Dialog", "如非本人登录，请修改密码"))
        if self.type =='KICK OUT':
            self.label.setText(_translate("Dialog", "该账户已在另一客户端登录,您将被愉悦送走"))
            self.label_2.setText(_translate("Dialog", "如非本人操作，请修改密码"))


    def _close(self):
        """
        发送关闭信号给RegisterForm类，即关闭注册GUI
        同时关闭CloseDialog类，即关闭本窗口
        :param
        :return:
        """
        self.close_signal.emit()
        self.close()




class Ui_Biography(object):
    def setupUi(self, Biography):
        Biography.setObjectName("Biography")
        Biography.resize(400, 400)
        Biography.setMinimumSize(QtCore.QSize(400, 400))
        Biography.setMaximumSize(QtCore.QSize(400, 400))
        Biography.setMouseTracking(True)
        Biography.setAnimated(True)
        Biography.setDocumentMode(False)
        Biography.setTabShape(QtWidgets.QTabWidget.Rounded)
        # 设置成无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(Biography)
        self.centralwidget.setObjectName("centralwidget")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(270, 160, 93, 28))
        self.addButton.setObjectName("addButton")
        self.portraitLabel = QtWidgets.QLabel(self.centralwidget)
        self.portraitLabel.setGeometry(QtCore.QRect(240, 10, 141, 141))
        self.portraitLabel.setText("")
        self.portraitLabel.setObjectName("portraitLabel")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(20, 40, 72, 15))
        self.nameLabel.setObjectName("nameLabel")
        self.animeLabel = QtWidgets.QLabel(self.centralwidget)
        self.animeLabel.setGeometry(QtCore.QRect(20, 100, 91, 16))
        self.animeLabel.setObjectName("animeLabel")
        self.bioLabel = QtWidgets.QLabel(self.centralwidget)
        self.bioLabel.setGeometry(QtCore.QRect(20, 220, 72, 15))
        self.bioLabel.setObjectName("bioLabel")
        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setGeometry(QtCore.QRect(90, 40, 91, 16))
        self.usernameLabel.setObjectName("usernameLabel")
        self.useranimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.useranimeLabel.setGeometry(QtCore.QRect(40, 140, 151, 20))
        self.useranimeLabel.setObjectName("useranimeLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 250, 251, 111))
        self.label.setObjectName("label")
        Biography.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Biography)
        self.statusbar.setObjectName("statusbar")
        Biography.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(Biography)
        self.toolBar.setObjectName("toolBar")
        Biography.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("resources/pic/助手与凶真.jpg").scaled(400,400)))
        self.setPalette(palette)
        self.setWindowOpacity(0.9)



        self.retranslateUi(Biography)
        QtCore.QMetaObject.connectSlotsByName(Biography)

    def retranslateUi(self, Biography):
        _translate = QtCore.QCoreApplication.translate
        Biography.setWindowTitle(_translate("Biography", "MainWindow"))
        self.addButton.setText(_translate("Biography", "添加好友"))
        self.nameLabel.setText(_translate("Biography", "用户名："))
        self.animeLabel.setText(_translate("Biography", "喜欢的动漫："))
        self.bioLabel.setText(_translate("Biography", "个人介绍："))
        self.usernameLabel.setText(_translate("Biography", "test"))
        self.useranimeLabel.setText(_translate("Biography", "Steins Gate"))
        self.label.setText(_translate("Biography", "EL PSY KONGROO"))
        self.toolBar.setWindowTitle(_translate("Biography", "toolBar"))




class Biography(QMainWindow, Ui_Biography):
    # pyqtSignal 要定义为一个类而不是属性，不能放到__init__里
    close_signal = QtCore.pyqtSignal()

    def __init__(self, userinfo):
        """
        注意close_signal 要在类成员函数外定义
        初始化CloseDialog类，将 确定 和 取消 按钮连接到self._close函数
        :param
        :return:
        """
        super(Biography, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.userinfo = userinfo
        self.addButton.clicked.connect(self.addFriend)
        self.portraitLabel.setText("")
        self.portraitLabel.setPixmap(QtGui.QPixmap("resources/pic/助手1.jpg").scaled(141, 141))
        self._set()
        self.addApply = AddApply()
        # 点击个人简介外的地方则关闭个人简介
        # 激活窗口，这样在点击母窗口的时候，eventFilter里会捕获到WindowDeactivate事件，从而关闭窗口
        self.activateWindow()
        self.installEventFilter(self)


    def _set(self):
        self.usernameLabel.setText(self.userinfo['name'])
        self.useranimeLabel.setText(self.userinfo['anime'])
        # 设置用户头像
        pass

    def addFriend(self):
        self.addApply.show()

    def eventFilter(self, obj, event):
        """
        事件过滤
        """
        if event.type() == QEvent.WindowDeactivate:
            self.close()  # 点击其他程序窗口，会关闭该对话框
            return True
        else:
            return super(Biography, self).eventFilter(obj, event)

    def _close(self):
        self.close_signal.emit()
        self.close()


class AddApply:
    pass