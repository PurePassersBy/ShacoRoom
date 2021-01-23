# -*- coding: utf-8 -*-

import sys
import pymysql
# 从mail模块中获得系统生成的验证码
from authentication.verifyGUI import Ui_Verify
from authentication.mailVerify import Mail
from PyQt5.QtWidgets import QApplication, QMainWindow
#导入designer工具生成的模块

class MyMainForm(QMainWindow, Ui_Verify):
    def __init__(self, senderMail):
        super(MyMainForm, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.senderMail=senderMail
        self.verifyCode=None
        # 添加检测验证码文本变化信号和槽
        self.sendButton.clicked.connect(self.send)
        self.codeEdit.textChanged['QString'].connect(self.statusBrowser.display)
        self.confirmButton.clicked.connect(self.update)          # 添加退出按钮信号和槽。调用close函数

    def send(self):
        mailAddress = self.mailEdit.text()
        sendMail = Mail(self.senderMail,"rduygnlorlpgbeec",mailAddress)
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


if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm("614446871@qq.com")
    #将窗口控件显示在屏幕上
    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
