# -*- coding: utf-8 -*-

import sys
import time
from authentication.dataBase import conn
# 从mail模块中获得系统生成的验证码
from authentication.verifyGUI import Ui_Verify
from authentication.mailVerify import Mail
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime , QObject
#导入designer工具生成的模块

class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currTime))
            time.sleep(1)

class MyMainForm(QMainWindow, Ui_Verify):
    def __init__(self, senderMail,passwordMail):
        super(MyMainForm, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.senderMail=senderMail
        self.passwordMail=passwordMail
        #验证码是否正确的标志
        self.flag=False
        #储存用户输入的验证码、用户名、密码、邮箱
        self.verifyCode=None
        self.name=None
        self.password=None
        self.mail=None

        # 添加检测验证码文本变化信号和槽 name password主要检测长度
        self.nameEdit.textChanged['QString'].connect(self.nameCheck)
        self.passwordEdit.textChanged['QString'].connect(self.passwordCheck)
        # 检测验证码是否正确
        self.codeEdit.textChanged['QString'].connect(self.codeCheck)
        #点击发送验证邮件按钮 调用send函数
        self.sendButton.clicked.connect(self.send)
        self.confirmButton.clicked.connect(self.update)


    def nameCheck(self):
        name = self.nameEdit.text()
        if len(name)>=9:
            print("Too long")
            self.nameStatus.setText("Too long")
        else:
            print("Right！")
            self.nameStatus.setText("Ok")
    def passwordCheck(self):
        password = self.passwordEdit.text()
        if len(password )>=12:
            print("Too long")
            self.passwordStatus.setText("Too long")
        else:
            print("Right！")
            self.passwordStatus.setText("Ok")

    def codeCheck(self):
        code= self.codeEdit.text()
        if code !=self.verifyCode:
            print("Wrong verify code!")
            self.codeStatus.setText("Wrong verify code!")
        else:
            print("Right！")
            self.codeStatus.setText("Ok")

    def send(self):
        #获取用户输入的邮箱地址
        mailAddress = str(self.mailEdit.text())
        print("test1")
        print(self.senderMail+"   "+self.passwordMail)
        sendMail = Mail(self.senderMail, self.passwordMail, mailAddress)
        print("test2")
        if sendMail.send():
            print("Send successfullly!")
            #储存系统生成的验证码 用于检验
            self.verifyCode=sendMail.verifyCode
        else:
            print("Send failed")
            self.failDisplay()


    def display(self):
        # 利用line Edit控件对象text()函数获取界面输入

        verifyCodeUser = self.codeEdit.text()
        # 利用text Browser控件对象setText()函数设置界面显示
        if verifyCodeUser==self.varifyCode:
            self.user_textBrowser.setText("验证成功")
        else:
            self.user_texBrowser.setText("验证码错误")
    def failDisplay(self):
        self.user_textBrowser.setText("邮件发送失败，请联系管理员")

    def update(self):
        #初始化封装在dataBase的连接
        connect=conn()
        connect.insert(self.name, self.mail, self.password)
        connect.close()



if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化用于发送验证邮件的邮箱 以及STMP服务授权码
    myWin = MyMainForm("614446871@qq.com","rduygnlorlpgbeec")
    #将窗口控件显示在屏幕上
    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
