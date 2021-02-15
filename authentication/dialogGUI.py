# -*- coding: utf-8 -*-
import pickle
import struct
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter, QIcon, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidgetItem, QLabel, QHBoxLayout, QWidget

sys.path.append('..')
from authentication.constantName import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        icon = QIcon()
        icon.addPixmap(QPixmap("../gui/resource/shaco_logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.setMaximumSize(QtCore.QSize(400, 300))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
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

        # 设置背景
        self.backgroundLabel = QtWidgets.QLabel(Dialog)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.backgroundLabel.setPixmap(QtGui.QPixmap("resources/pic/whiteBackground.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.lower()

        self.setQSS()

    def setQSS(self):
        button_qss = '''     QDialogButtonBox{  
                                     border:2px solid #F3F3F5;   
                                     color:black;         
                                     font-size:12px;         
                                     height:40px;         
                                     padding-left:5px;         
                                     padding-right:10px;         
                                     }     
                                               QDialogButtonBox:hover{         
                                     color:brown;         
                                     border:2px solid #F3F3F5;         
                                     border-radius:10px;         
                                     background:LightGray;     
                                     } '''
        self.buttonBox.setStyleSheet(button_qss)

        label_qss = '''QLabel{
                                        color:black
                                        }
                                        QLabel:hover{
                                        color:gray
                                        }
                            '''
        self.label.setStyleSheet(label_qss)
        self.label_2.setStyleSheet(label_qss)

        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "系统通知"))
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
        if self.type == 'EDIT SUCCESS':
            self.label.setText(_translate("Dialog", "密码修改成功！"))
            self.label_2.setText(_translate("Dialog", "注意保管好密码哦"))
        if self.type == SYSTEM_CODE_LOGIN_REPEAT:
            self.label.setText(_translate("Dialog", "该账户已登录"))
            self.label_2.setText(_translate("Dialog", "如非本人登录，请修改密码"))
        if self.type == SYSTEM_CODE_KICK_OUT:
            self.label.setText(_translate("Dialog", "该账户已在另一客户端登录,您将被愉悦送走"))
            self.label_2.setText(_translate("Dialog", "如非本人操作，请修改密码"))
        if self.type == 'UNDER CONSTRUCTION':
            self.label.setText(_translate("Dialog", "该功能正在施工中"))
            self.label_2.setText(_translate("Dialog", "敬请期待"))

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
        self.centralwidget = QtWidgets.QWidget(Biography)
        self.centralwidget.setObjectName("centralwidget")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(230, 160, 70, 28))
        self.deleteButton.setObjectName("deleteButton")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(320, 160, 70, 25))
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
        self.usernameLabel.setGeometry(QtCore.QRect(90, 40, 120, 16))
        self.usernameLabel.setObjectName("usernameLabel")
        self.useranimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.useranimeLabel.setGeometry(QtCore.QRect(40, 140, 180, 40))
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
        self.toolBar.setVisible(False)
        self.statusbar.setVisible(False)

        self.setStyleSheet("background-color:rgb(255,255,255);")
        # 绘制边框
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(5, 0, 10, 400))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(390, 0, 10, 400))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(0, 390, 400, 10))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(0, 0, 400, 10))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(80, 200, 230, 10))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")

        self.setQSS()
        self.retranslateUi(Biography)
        QtCore.QMetaObject.connectSlotsByName(Biography)

    def setQSS(self):
        button_qss = '''     QPushButton{
                                     border:2px solid #F3F3F5;
                                     color:green;
                                     font-size:12px;
                                     height:40px;
                                     padding-left:5px;
                                     padding-right:10px;
                                     background:LightGray;
                                     }
                                               QPushButton:hover{
                                     color:cyan;
                                     border:2px solid #F3F3F5;
                                     border-radius:10px;
                                     background:Gray;
                                     } '''
        deletebutton_qss = '''     QPushButton{
                                     border:2px solid #F3F3F5;
                                     color:red;
                                     font-size:12px;
                                     height:40px;
                                     padding-left:5px;
                                     padding-right:10px;
                                     background:LightGray;
                                     }
                                               QPushButton:hover{
                                     color:orange;
                                     border:2px solid #F3F3F5;
                                     border-radius:10px;
                                     background:Gray;
                                     } '''
        self.addButton.setStyleSheet(button_qss)
        self.deleteButton.setStyleSheet(button_qss)
        self.deleteButton.setStyleSheet(deletebutton_qss)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def retranslateUi(self, Biography):
        _translate = QtCore.QCoreApplication.translate
        Biography.setWindowTitle(_translate("Biography", "MainWindow"))
        self.addButton.setText(_translate("Biography", "添加好友"))
        self.deleteButton.setText(_translate("Biography", "删除好友"))
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

    def __init__(self, self_id, self_name, target_id, x, y, db_conn, server_conn, private_chat, delete_friend):
        """
        注意close_signal 要在类成员函数外定义
        初始化CloseDialog类，将 确定 和 取消 按钮连接到self._close函数
        :param
        :return:
        """
        super(Biography, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setGeometry(x, y, 400, 400)
        self.self_id = self_id
        self.self_name = self_name
        self.target_id = target_id
        self.db_conn = db_conn
        self.server_conn = server_conn
        self.private_chat_func = private_chat
        self.delete_friend_func = delete_friend
        res = self.db_conn.search(TABLE_NAME_USERINFO, ['id', self.target_id])
        self.userinfo = res[0]
        self.friend_list = self.db_conn.search(TABLE_NAME_FRIENDINFO, ['id', self.self_id])
        self.deleteButton.setVisible(False)
        # 判断是否为自己或已添加的好友
        self.flag = True
        if self.self_id == self.target_id:
            self.addButton.setVisible(False)

        else:
            if self.friend_list is not None:
                for i in self.friend_list:
                    if i == self.target_id:
                        self.flag = False
                        break
            if self.flag is False:
                self.addButton.setText('私聊')
                self.addButton.clicked.connect(self.private_chat)
                self.deleteButton.setVisible(True)
                self.deleteButton.clicked.connect(self.delete_friend)
            if self.flag is True:
                self.addButton.clicked.connect(self.add_friend)

        self.portraitLabel.setText("")
        img = QPixmap(PORTRAIT_PATH % self.target_id).scaled(141, 141)
        self.portraitLabel.setPixmap(img)
        self._set()
        # 初始化添加好友窗口
        self.addApply = None
        # 初始化删除好友警告窗口
        self.delete_friend_window = None
        # 点击个人简介外的地方则关闭个人简介
        # 激活窗口，这样在点击母窗口的时候，eventFilter里会捕获到WindowDeactivate事件，从而关闭窗口
        self.activateWindow()
        self.installEventFilter(self)

    def _set(self):
        self.usernameLabel.setText(self.userinfo[1])
        self.useranimeLabel.setText(self.userinfo[4])

        # 设置自动换行
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameLabel.sizePolicy().hasHeightForWidth())
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setText(self.userinfo[5])

        sizePolicy.setHeightForWidth(self.useranimeLabel.sizePolicy().hasHeightForWidth())
        self.useranimeLabel.setSizePolicy(sizePolicy)
        self.useranimeLabel.setWordWrap(True)

        # 设置用户头像
        pass

    def private_chat(self):
        self.private_chat_func(self.target_id)

    def delete_friend(self):
        delete_warning = '确定要删除该好友吗？（对方会收到被删通知）'
        self.delete_friend_window = FriendApply(self.self_id, self.target_id, self.userinfo[1],
                                                delete_warning, self.server_conn)
        self.delete_friend_window.acceptButton.setText('取消')
        self.delete_friend_window.rejectButton.setText('爆杀！')
        self.delete_friend_window.applyLabel.setVisible(False)
        self.delete_friend_window.acceptButton.clicked.disconnect(self.delete_friend_window.accept)
        self.delete_friend_window.rejectButton.clicked.disconnect(self.delete_friend_window.reject)
        self.delete_friend_window.acceptButton.clicked.connect(self.delete_friend_window.close)
        self.delete_friend_window.rejectButton.clicked.connect(self.confirm_delete)
        self.delete_friend_window.rejectButton.clicked.connect(self.delete_friend_window.close)
        self.delete_friend_window.show()

    def confirm_delete(self):
        pack = {
            'send_id': self.self_id,
            'send_name': self.self_name,
            'target_id': self.target_id,
            'message': f'您已被用户 {self.self_name} 删除好友关系',
            'system_code': SYSTEM_CODE_DELETE_FRIEND
        }
        pack_str = pickle.dumps(pack)
        self.server_conn.send(struct.pack('i', len(pack_str)))
        self.server_conn.send(pack_str)
        self.db_conn.delete(TABLE_NAME_FRIENDINFO, [self.self_id, self.target_id])
        self.db_conn.delete(TABLE_NAME_FRIENDINFO, [self.target_id, self.self_id])
        self.delete_friend_func(self.target_id)
        self.close()
        print("?")

    def add_friend(self):
        # self.addApply = Dialog('UNDER CONSTRUCTION')
        # self.addApply.show()
        self.addApply = SendFriendApply(self.self_id, self.target_id, self.server_conn)
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


class Ui_SendApplyDialog(object):
    def setupUi(self, SendApplyDialog):
        SendApplyDialog.setObjectName("SendApplyDialog")
        SendApplyDialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(SendApplyDialog)
        self.buttonBox.setGeometry(QtCore.QRect(200, 250, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.titleLabel = QtWidgets.QLabel(SendApplyDialog)
        self.titleLabel.setGeometry(QtCore.QRect(10, 10, 72, 15))
        self.titleLabel.setObjectName("titleLabel")
        self.closeButton = QtWidgets.QPushButton(SendApplyDialog)
        self.closeButton.setGeometry(QtCore.QRect(370, 0, 93, 28))
        self.closeButton.setObjectName("closeButton")
        self.psLabel = QtWidgets.QLabel(SendApplyDialog)
        self.psLabel.setGeometry(QtCore.QRect(40, 230, 301, 16))
        self.psLabel.setObjectName("psLabel")
        self.textEdit = QtWidgets.QTextEdit(SendApplyDialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 70, 361, 151))
        self.textEdit.setObjectName("textEdit")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        # 设置背景
        self.backgroundLabel = QtWidgets.QLabel(SendApplyDialog)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.backgroundLabel.setPixmap(QtGui.QPixmap("resources/pic/whiteBackground.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.lower()

        self.setQSS()
        self.retranslateUi(SendApplyDialog)
        QtCore.QMetaObject.connectSlotsByName(SendApplyDialog)

    def setQSS(self):
        self.closeButton.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.closeButton.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')

        button_qss = '''     QDialogButtonBox{
                                     border:2px solid #F3F3F5;
                                     color:black;
                                     font-size:12px;
                                     height:40px;
                                     padding-left:5px;
                                     padding-right:10px;
                                     }
                                               QDialogButtonBox:hover{
                                     color:brown;
                                     border:2px solid #F3F3F5;
                                     border-radius:10px;
                                     background:LightGray;
                                     } '''
        self.buttonBox.setStyleSheet(button_qss)

        label_qss = '''QLabel{color:gray}'''
        self.psLabel.setStyleSheet(label_qss)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def retranslateUi(self, SendApplyDialog):
        _translate = QtCore.QCoreApplication.translate
        SendApplyDialog.setWindowTitle(_translate("ApplyDialog", "添加好友"))
        self.titleLabel.setText(_translate("ApplyDialog", "添加好友"))
        self.closeButton.setText(_translate("ApplyDialog", " "))
        self.psLabel.setText(_translate("ApplyDialog", "需对方同意好友申请，才能成为好友"))


class SendFriendApply(QMainWindow, Ui_SendApplyDialog):

    def __init__(self, self_id, target_id, server_conn):
        """
        发送好友请求的界面
        :param
        :return:
        """
        super(SendFriendApply, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.self_id = self_id
        self.target_id = target_id
        self.server_conn = server_conn
        self.buttonBox.accepted.connect(self.send)
        self.buttonBox.rejected.connect(self.close)
        self.closeButton.clicked.connect(self.close)
        self.dialog = None

    def send(self):
        # self.dialog = Dialog('UNDER CONSTRUCTION')
        # self.dialog.show()
        pack = {
            'system_code': SYSTEM_CODE_FRIEND_APPLY,
            'send_id': self.self_id,
            'target_id': self.target_id,
            'message': self.textEdit.toPlainText()
        }
        pack_str = pickle.dumps(pack)
        self.server_conn.send(struct.pack('i', len(pack_str)))
        self.server_conn.send(pack_str)
        self.close()


class Ui_ApplyDialog(object):
    def setupUi(self, ApplyDialog):
        ApplyDialog.setObjectName("ApplyDialog")
        ApplyDialog.resize(400, 300)
        ApplyDialog.setMinimumSize(QtCore.QSize(400, 300))
        ApplyDialog.setMaximumSize(QtCore.QSize(400, 300))
        icon = QIcon()
        icon.addPixmap(QPixmap("../gui/resource/shaco_logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.portraitLabel = QtWidgets.QLabel(ApplyDialog)
        self.portraitLabel.setGeometry(QtCore.QRect(0, 10, 100, 100))
        self.portraitLabel.setText("")
        self.portraitLabel.setPixmap(QtGui.QPixmap("resources/pic/助手3.jpg"))
        self.portraitLabel.setScaledContents(True)
        self.portraitLabel.setObjectName("portraitLabel")
        self.acceptButton = QtWidgets.QPushButton(ApplyDialog)
        self.acceptButton.setGeometry(QtCore.QRect(40, 260, 93, 28))
        self.acceptButton.setObjectName("acceptButton")
        self.rejectButton = QtWidgets.QPushButton(ApplyDialog)
        self.rejectButton.setGeometry(QtCore.QRect(280, 260, 93, 28))
        self.rejectButton.setObjectName("rejectButton")
        self.textLabel = QtWidgets.QLabel(ApplyDialog)
        self.textLabel.setGeometry(QtCore.QRect(40, 120, 321, 121))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel.sizePolicy().hasHeightForWidth())
        self.textLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.textLabel.setFont(font)
        self.textLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.textLabel.setWordWrap(True)
        self.textLabel.setObjectName("textLabel")
        self.nameLabel = QtWidgets.QLabel(ApplyDialog)
        self.nameLabel.setGeometry(QtCore.QRect(110, 20, 220, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")

        self.applyLabel = QtWidgets.QLabel(ApplyDialog)
        self.applyLabel.setGeometry(QtCore.QRect(320, 70, 80, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.applyLabel.setFont(font)
        self.applyLabel.setObjectName("applyLabel")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        # 设置背景
        self.backgroundLabel = QtWidgets.QLabel(ApplyDialog)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.backgroundLabel.setPixmap(QtGui.QPixmap("resources/pic/whiteBackground.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.lower()
        self.setQSS()
        self.retranslateUi(ApplyDialog)
        QtCore.QMetaObject.connectSlotsByName(ApplyDialog)

    def setQSS(self):
        self.acceptButton.setFixedSize(80, 40)  # 设置接受按钮的大小
        self.rejectButton.setFixedSize(80, 40)  # 设置拒绝按钮的大小
        accept_button_qss = '''     QPushButton{
                 border:none;         
                 color:black;         
                 font-size:15px;         
                 height:40px;         
                 padding-left:5px;         
                 padding-right:10px;  
                 background:LightGreen;       
                 }     
                            QPushButton:hover{         
                 color:LightGray;         
                 border:1px solid #F3F3F5;         
                 border-radius:10px;
                                  font-size:15px;         
                 height:40px;         
                 padding-left:5px;         
                 padding-right:10px;           
                 background:green;  
                 } '''
        rejept_button_qss = '''     QPushButton{
                 border:none;         
                 color:black;         
                 font-size:15px;         
                 height:40px;         
                 padding-left:5px;         
                 padding-right:10px;  
                 background:orange;       
                 }     
                            QPushButton:hover{         
                 color:LightGray;         
                 border:1px solid #F3F3F5;         
                 border-radius:10px;
                                  font-size:15px;         
                 height:40px;         
                 padding-left:5px;         
                 padding-right:10px;           
                 background:red;     
                 } '''
        self.acceptButton.setStyleSheet(accept_button_qss)
        self.rejectButton.setStyleSheet(rejept_button_qss)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.98)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def retranslateUi(self, ApplyDialog):
        _translate = QtCore.QCoreApplication.translate
        ApplyDialog.setWindowTitle(_translate("ApplyDialog", "好友申请"))
        self.acceptButton.setText(_translate("ApplyDialog", "接受"))
        self.rejectButton.setText(_translate("ApplyDialog", "拒绝"))
        self.textLabel.setText(_translate("ApplyDialog", "TextLabel"))
        self.nameLabel.setText(_translate("ApplyDialog", "TextLabel"))
        self.applyLabel.setText(_translate("ApplyDialog", "好友申请"))


class FriendApply(QMainWindow, Ui_ApplyDialog):
    accept_signal = QtCore.pyqtSignal(int, str)

    def __init__(self, self_id, send_id, send_name, message, server_conn):
        """
        处理好友请求的窗口
        """
        super(FriendApply, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.self_id = self_id
        self.send_id = send_id
        self.message = message
        self.send_name = send_name
        self.server_conn = server_conn
        img = QPixmap(PORTRAIT_PATH % self.send_id).scaled(100, 100)
        self.portraitLabel.setPixmap(img)
        self.textLabel.setText(self.message)
        self.nameLabel.setText(self.send_name)
        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton.clicked.connect(self.reject)

    def accept(self):
        pack = {
            'system_code': SYSTEM_CODE_RESULT_FRIEND_APPLY,
            'send_id': self.self_id,
            'target_id': self.send_id,
            'message': 'ACCEPT'
        }
        pack_str = pickle.dumps(pack)
        self.server_conn.send(struct.pack('i', len(pack_str)))
        self.server_conn.send(pack_str)
        self.accept_signal.emit(int(self.send_id), str(self.send_name))
        self.close()

    def reject(self):
        pack = {
            'system_code': SYSTEM_CODE_RESULT_FRIEND_APPLY,
            'send_id': self.self_id,
            'target_id': self.send_id,
            'message': 'REJECT'
        }
        pack_str = pickle.dumps(pack)
        self.server_conn.send(struct.pack('i', len(pack_str)))
        self.server_conn.send(pack_str)
        self.close()


class Ui_ApplyResultDialog(object):
    def setupUi(self, ApplyResultDialog):
        ApplyResultDialog.setObjectName("ApplyResultDialog")
        ApplyResultDialog.resize(400, 300)
        ApplyResultDialog.setMinimumSize(QtCore.QSize(400, 300))
        ApplyResultDialog.setMaximumSize(QtCore.QSize(400, 300))
        icon = QIcon()
        icon.addPixmap(QPixmap("../gui/resource/shaco_logo.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.portraitLabel = QtWidgets.QLabel(ApplyResultDialog)
        self.portraitLabel.setGeometry(QtCore.QRect(0, 10, 100, 100))
        self.portraitLabel.setText("")
        self.portraitLabel.setPixmap(QtGui.QPixmap("resources/pic/助手3.jpg"))
        self.portraitLabel.setScaledContents(True)
        self.portraitLabel.setObjectName("portraitLabel")
        self.confirmButton = QtWidgets.QPushButton(ApplyResultDialog)
        self.confirmButton.setGeometry(QtCore.QRect(180, 260, 93, 28))
        self.confirmButton.setObjectName("confirmButton")
        self.textLabel = QtWidgets.QLabel(ApplyResultDialog)
        self.textLabel.setGeometry(QtCore.QRect(40, 120, 321, 121))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel.sizePolicy().hasHeightForWidth())
        self.textLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.textLabel.setFont(font)
        self.textLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.textLabel.setWordWrap(True)
        self.textLabel.setObjectName("textLabel")
        self.nameLabel = QtWidgets.QLabel(ApplyResultDialog)
        self.nameLabel.setGeometry(QtCore.QRect(120, 30, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        # 设置背景
        self.backgroundLabel = QtWidgets.QLabel(ApplyResultDialog)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.backgroundLabel.setPixmap(QtGui.QPixmap("resources/pic/whiteBackground.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.lower()

        self.retranslateUi(ApplyResultDialog)
        QtCore.QMetaObject.connectSlotsByName(ApplyResultDialog)

    def setQSS(self):
        self.confirmButton.setFixedSize(30, 20)  # 设置接受按钮的大小
        self.confirmButton.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.98)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def retranslateUi(self, ApplyResultDialog):
        _translate = QtCore.QCoreApplication.translate
        ApplyResultDialog.setWindowTitle(_translate("ApplyDialog", "好友申请结果"))
        self.confirmButton.setText(_translate("ApplyDialog", "确定"))
        self.textLabel.setText(_translate("ApplyDialog", "TextLabel"))
        self.nameLabel.setText(_translate("ApplyDialog", "TextLabel"))


class ResultFriendApply(QMainWindow, Ui_ApplyResultDialog):
    def __init__(self, self_id, send_id, send_name, message, PORTRAIT_PATH):
        """
        处理好友请求的窗口
        """
        super(ResultFriendApply, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.self_id = self_id
        self.send_id = send_id
        self.send_name = send_name
        img = QPixmap(PORTRAIT_PATH % self.send_id).scaled(100, 100)
        self.portraitLabel.setPixmap(img)
        self.nameLabel.setText(self.send_name)
        self.confirmButton.clicked.connect(self.close)
        if message == 'ACCEPT':
            self.textLabel.setText(f'{send_name}接受了您的好友请求')
        elif message == 'REJECT':
            self.textLabel.setText(f'{send_name}拒绝了您的好友请求')
        else:
            self.textLabel.setText(f'{send_name}解除了与您的好友关系')

class Ui_FriendProcessWindow(object):
    def setupUi(self, FriendProcessWindow):
        FriendProcessWindow.setObjectName("FriendProcessWindow")
        FriendProcessWindow.resize(300, 500)
        FriendProcessWindow.setMinimumSize(QtCore.QSize(300, 500))
        FriendProcessWindow.setMaximumSize(QtCore.QSize(300, 500))
        font = QtGui.QFont()
        font.setPointSize(9)
        FriendProcessWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(FriendProcessWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(10, 10, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 30, 300, 430))
        self.listWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidget.setObjectName("listWidget")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(275, 0, 20, 20))
        self.closeButton.setObjectName("closeButton")
        self.emptyLabel = QtWidgets.QLabel(self.centralwidget)
        self.emptyLabel.setGeometry(QtCore.QRect(70, 90, 171, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.emptyLabel.setFont(font)
        self.emptyLabel.setObjectName("emptyLabel")
        FriendProcessWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FriendProcessWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 26))
        self.menubar.setObjectName("menubar")
        FriendProcessWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FriendProcessWindow)
        self.statusbar.setObjectName("statusbar")
        FriendProcessWindow.setStatusBar(self.statusbar)

        # 设置背景
        self.backgroundLabel = QtWidgets.QLabel(FriendProcessWindow)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, 300, 500))
        self.backgroundLabel.setPixmap(QtGui.QPixmap("resources/pic/whiteBackground.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.lower()
        self.setQSS()

        self.retranslateUi(FriendProcess)
        QtCore.QMetaObject.connectSlotsByName(FriendProcessWindow)

    def setQSS(self):
        self.closeButton.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.closeButton.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')

        label_qss = '''QLabel{
                    color:LightGray
                    }
                    QLabel:hover{
                    color:gray
                    }
        '''
        self.emptyLabel.setStyleSheet(label_qss)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def retranslateUi(self, FriendProcessWindow):
        _translate = QtCore.QCoreApplication.translate
        self.titleLabel.setText(_translate("FriendProcessWindow", "好友处理"))
        self.closeButton.setText(_translate("FriendProcessWindow", " "))
        self.emptyLabel.setText(_translate("FriendProcessWindow", "空空如也0.0"))


class MYWidget(QWidget):
    clicked_deal_signal = pyqtSignal(int)
    clicked_show_signal = pyqtSignal(dict)

    def __init__(self, user_dict, parent=None):
        super().__init__(parent)
        self.user_dict = user_dict
        self.user_id = user_dict['send_id']

    def mousePressEvent(self, QMouseEvent):
        self.clicked_deal_signal.emit(self.user_id)
        self.clicked_show_signal.emit(self.user_dict)

class FriendProcess(QMainWindow, Ui_FriendProcessWindow):
    def __init__(self, to_do_list, system_code_func):
        super(FriendProcess, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.titleLabel.setVisible(True)
        self.closeButton.clicked.connect(self.close)
        self.system_code_func = system_code_func
        self.system_code2chinese = {SYSTEM_CODE_FRIEND_APPLY: '好友申请',
                                    SYSTEM_CODE_RESULT_FRIEND_APPLY: '好友申请结果',
                                    SYSTEM_CODE_RESULT_DELETE_FRIEND: '解除好友关系',
                                    }
        if to_do_list:
            self.emptyLabel.setVisible(False)
        else:
            self.emptyLabel.setVisible(True)
        # 加载待处理信息
        for i in to_do_list:
            self.add_deal(i)





    def add_deal(self, user_dict):
        item = QListWidgetItem()
        widget = MYWidget(user_dict)
        widget.clicked_deal_signal.connect(self.delete_deal)
        widget.clicked_show_signal.connect(self.system_code_func)
        layout = QHBoxLayout()
        portrait_path = PORTRAIT_PATH % user_dict['send_id']
        img = QPixmap(portrait_path).scaled(30, 30)
        portrait = QLabel()
        portrait.setPixmap(img)
        layout.addWidget(portrait)
        layout.addWidget(QLabel(user_dict['send_name']))
        layout.addWidget(QLabel(self.system_code2chinese[user_dict['system_code']]))
        layout.setStretch(3, 5)
        widget.setLayout(layout)
        item.setSizeHint(QSize(300, 60))
        self.todoList.addItem(item)
        self.todoList.setItemWidget(item, widget)

    def delete_deal(self, user_id):
        for index in range(self.todoList.count()):
            item = self.to_do_list.item(index)
            widget = self.todoList.itemWidget(item)
            if widget.user_id == user_id:
                self.todoList.takeItem(index)
                del item
                break

