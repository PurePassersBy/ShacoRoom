# -*- coding: utf-8 -*-
import sys
import random

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon, QTextCursor
from PyQt5 import QtWidgets, QtCore


from mailVerify import Mail
from DAO.dataBase import Connect
from verifyGUI import Ui_Verify
from loginGUI import Ui_login


# 导入designer工具生成的模块

class MyMainForm(QMainWindow, Ui_Verify):
    def __init__(self, senderMail, passwordMail):
        super(MyMainForm, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.senderMail = senderMail
        self.passwordMail = passwordMail
        # 验证码是否正确的标志
        self.flag = False
        # 储存用户输入的验证码、用户名、密码、邮箱
        self.verifyCode = None

        # 添加检测验证码文本变化信号和槽 name password主要检测长度
        self.nameEdit.textChanged['QString'].connect(self.nameCheck)
        self.nameEdit.setToolTip('长度不超过8')
        self.passwordEdit.textChanged['QString'].connect(self.passwordCheck)
        self.passwordEdit.setToolTip('长度不超过12')
        # 检测验证码是否正确
        self.codeEdit.textChanged['QString'].connect(self.codeCheck)
        # 点击发送验证邮件按钮 调用send函数
        self.sendButton.clicked.connect(self.send)
        self.confirmButton.clicked.connect(self.updateUserinfo)

    def nameCheck(self):
        name = self.nameEdit.text()
        if len(name) > 8:
            self.nameStatus.setText("Too long")
        else:
            self.nameStatus.setText("Ok")

    def passwordCheck(self):
        password = self.passwordEdit.text()
        if len(password) > 12:
            self.passwordStatus.setText("Too long")
        else:
            self.passwordStatus.setText("Ok")

    def codeCheck(self):
        code = int(self.codeEdit.text())
        if code != self.verifyCode:
            self.codeStatus.setText("Wrong")

        else:
            # 确认用户邮箱
            self.flag = True
            print("Right verify code!")
            self.codeStatus.setText("Ok")

    def send(self):
        # 获取用户输入的邮箱地址
        mailAddress = str(self.mailEdit.text())
        # 检测用户邮箱是否注册
        connect = Connect()
        mail_repeat = connect.search('mail', mailAddress)
        # 关闭与mysql的连接
        connect.close()

        if mail_repeat is None:
            # 邮箱合法
            print("邮箱合法")
            self.verifyCode = self.generateCode()
            print(self.senderMail + "   " + self.passwordMail + "verify code:" + str(self.verifyCode))
            sendMail = Mail(self.senderMail, self.passwordMail, mailAddress, self.verifyCode)
            # 用线程发送邮件 避免用户等待
            sendMail.start()
        else:
            # 邮箱重复
            print("邮箱重复")
            self.mailStatus.setText("该邮箱已被注册！")

    def generateCode(self):
        code = random.randint(100000, 999999)  # 生成六位随机数
        return code

    def updateUserinfo(self):
        # 初始化封装在dataBase的连接
        mailEnter = str(self.mailEdit.text())
        nameEnter = str(self.nameEdit.text())
        passwordEnter = str(self.passwordEdit.text())
        print(mailEnter)
        if self.flag:
            connect = Connect()
            # 将用户信息添加到数据库

            connect.insert(nameEnter, mailEnter, passwordEnter)
            connect.close()
        else:
            self.codeStatus.setText("未收到邮件？请检查邮箱是否输入错误")
            pass


class LoginForm(QMainWindow, Ui_login):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.mail = None
        self.password = None
        # 添加检测验证码文本变化信号和槽 mil password主要检测长度
        self.mailEdit.textChanged['QString'].connect(self._mail_check)
        self.mailEdit.setToolTip('没有邮箱？请先注册')

        self.passwordEdit.textChanged['QString'].connect(self._password_check)
        self.passwordEdit.setToolTip('长度不超过12')
        # 点击发送验证邮件按钮 调用send函数
        self.loginButton.clicked.connect(self._login)
        self.registerButton.clicked.connect(self._register)
        self.qt_register = MyMainForm("614446871@qq.com", "rduygnlorlpgbeec")

    def _mail_check(self):
        mail = str(self.mailEdit.text())
        if len(mail) > 20:
            self.mailStatus.setText('Too long')
        else:
            self.mailStatus.setText('Oook')

    def _password_check(self):
        password = str(self.passwordEdit.text())
        if len(password) > 12:
            self.passwordStatus.setText('Too long')
        else:
            self.passwordStatus.setText('Oook')

    def _login(self):
        self.mail = str(self.mailEdit.text())
        self.password = str(self.passwordEdit.text())
        # 连接数据库
        conn = Connect()
        result = conn.search('mail', self.mail)
        if result is None:
            self.mailStatus.setText('该邮箱未注册，请先注册')
        else:
            # result 返回的是一个二维tuple
            if result[0][3] == self.password:
                self.passwordStatus.setText('密码正确')
                # 接入聊天室
                pass
            else:
                self.passwordStatus.setText('密码错误')
        # 关闭数据库连接
        conn.close()

    def _register(self):
        # 跳转到注册界面
        self.qt_register.show()


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化用于发送验证邮件的邮箱 以及STMP服务授权码
    myWin = LoginForm()
    # 将窗口控件显示在屏幕上
    myWin.show()

    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
