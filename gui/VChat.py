# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/VChat.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(732, 774)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Shaco_Logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(40, 80, 481, 111))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(430, 190, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(550, 10, 171, 192))
        self.graphicsView.setStyleSheet("")
        self.graphicsView.setObjectName("graphicsView")
        self.label_username = QtWidgets.QLabel(Form)
        self.label_username.setGeometry(QtCore.QRect(550, 220, 171, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_username.setFont(font)
        self.label_username.setAlignment(QtCore.Qt.AlignCenter)
        self.label_username.setObjectName("label_username")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(550, 270, 171, 471))
        self.listView.setObjectName("listView")
        self.label_friends = QtWidgets.QLabel(Form)
        self.label_friends.setGeometry(QtCore.QRect(600, 280, 72, 15))
        self.label_friends.setAlignment(QtCore.Qt.AlignCenter)
        self.label_friends.setObjectName("label_friends")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 10, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.msg_list = QtWidgets.QListWidget(Form)
        self.msg_list.setGeometry(QtCore.QRect(40, 240, 481, 501))
        self.msg_list.setObjectName("msg_list")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.send_message)
        self.pushButton_2.clicked.connect(Form.user_setting)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ShacoRoom"))
        self.pushButton.setText(_translate("Form", "发送"))
        self.label_username.setText(_translate("Form", "TextLabel"))
        self.label_friends.setText(_translate("Form", "好友列表"))
        self.pushButton_2.setText(_translate("Form", "设置"))
import gui.resources_rc
