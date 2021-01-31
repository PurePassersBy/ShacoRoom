# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(800, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Shaco_Logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        login.setWindowIcon(icon)
        login.setStyleSheet("")
        login.setMinimumSize(QtCore.QSize(800, 500))
        login.setMaximumSize(QtCore.QSize(900, 500))
        self.loginButton = QtWidgets.QPushButton(login)
        self.loginButton.setGeometry(QtCore.QRect(120, 420, 93, 28))
        self.loginButton.setObjectName("loginButton")
        self.registerButton = QtWidgets.QPushButton(login)
        self.registerButton.setGeometry(QtCore.QRect(320, 420, 93, 28))
        self.registerButton.setObjectName("registerButton")
        self.titleLabel = QtWidgets.QLabel(login)
        self.titleLabel.setGeometry(QtCore.QRect(170, 30, 150, 150))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setMinimumSize(QtCore.QSize(150, 150))
        self.titleLabel.setMaximumSize(QtCore.QSize(150, 150))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.titleLabel.setMouseTracking(False)
        self.titleLabel.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.titleLabel.setObjectName("titleLabel")
        self.mailLabel = QtWidgets.QLabel(login)
        self.mailLabel.setGeometry(QtCore.QRect(40, 240, 72, 15))
        self.mailLabel.setObjectName("mailLabel")
        self.passwordLabel = QtWidgets.QLabel(login)
        self.passwordLabel.setGeometry(QtCore.QRect(40, 320, 72, 15))
        self.passwordLabel.setObjectName("passwordLabel")
        self.passwordStatus = QtWidgets.QLabel(login)
        self.passwordStatus.setGeometry(QtCore.QRect(110, 360, 321, 20))
        self.passwordStatus.setText("")
        self.passwordStatus.setObjectName("passwordStatus")
        self.mailStatus = QtWidgets.QLabel(login)
        self.mailStatus.setGeometry(QtCore.QRect(120, 270, 311, 21))
        self.mailStatus.setObjectName("mailStatus")
        self.mailEdit = QtWidgets.QLineEdit(login)
        self.mailEdit.setGeometry(QtCore.QRect(110, 230, 300, 30))
        self.mailEdit.setObjectName("mailEdit")
        self.passwordEdit = QtWidgets.QLineEdit(login)
        self.passwordEdit.setGeometry(QtCore.QRect(110, 310, 300, 30))
        self.passwordEdit.setObjectName("passwordEdit")
        self.label = QtWidgets.QLabel(login)
        self.label.setGeometry(QtCore.QRect(430, 20, 331, 251))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources/pic/shaco.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.mailLabel.raise_()
        self.passwordStatus.raise_()
        self.loginButton.raise_()
        self.passwordLabel.raise_()
        self.registerButton.raise_()
        self.titleLabel.raise_()
        self.mailStatus.raise_()
        self.mailEdit.raise_()
        self.passwordEdit.raise_()
        self.label.raise_()

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "ShacoRoom v1.0.0"))
        self.loginButton.setText(_translate("login", "登录"))
        self.registerButton.setText(_translate("login", "注册"))
        self.titleLabel.setText(_translate("login", "ShacoRoom"))
        self.mailLabel.setText(_translate("login", "邮箱"))
        self.passwordLabel.setText(_translate("login", "密码"))
        self.mailStatus.setText(_translate("login", " "))
