# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/VSettings.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(458, 297)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.lineEdit_username = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_username.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.verticalLayout_2.addWidget(self.lineEdit_username)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit_fav_comic = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_fav_comic.setObjectName("lineEdit_fav_comic")
        self.verticalLayout.addWidget(self.lineEdit_fav_comic)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(Dialog.load_file)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.pushButton.setText(_translate("Dialog", "修改头像"))
        self.label.setText(_translate("Dialog", "最喜欢的动漫"))
        self.label_2.setText(_translate("Dialog", "个人简介"))
