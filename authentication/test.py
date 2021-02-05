# -*- coding: utf-8 -*-
import sys
import time
import random
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow

sys.path.append('..')
from authentication.mailThread import Mail
from authentication.verifyGUI import Ui_Verify
from authentication.loginGUI import Ui_login
from authentication.editGUI import Ui_Edit
from authentication.dialogGUI import Dialog
from authentication.connecter.SQLConn import ConnectSQL
from gui.ChatGui import ChatGUI


class EditpasswordForm(QMainWindow, Ui_Edit):
    def __init__(self, sender_mail, password_mail, conn):
        """
        初始化LoginForm类，设置不同按钮连接的槽与信号函数
        实例化RegisterForm()类以便完成显示注册界面，并输入注册发送邮件的邮箱与stmp授权码
        :param:
        :return:
        """
        super(EditpasswordForm, self).__init__()
        # 实例化子类dialog,这一步一定要在self.initUi前面,不然initUi中不能调用没有实例化的close_signal这个槽信
        self.success_dialog = Dialog('EDIT SUCCESS')
        self.setupUi(self)
        self.retranslateUi(self)
        # 接收来自登陆界面的DAO connecter
        self.conn = conn
        # 储存发送邮箱以及邮箱stmp授权码
        self.senderMail = sender_mail
        self.passwordMail = password_mail
        # 验证码是否正确的标志
        self.flag = False
        # 储存生存的验证码
        self.verifyCode = None
        # 添加检测文本变化信号和槽 设置长度限制提示  设置最大输入字符数
        self.newpasswordEdit.textChanged['QString'].connect(self._newpassword_check)
        self.newpasswordEdit.setToolTip('长度不超过12')
        self.newpasswordEdit.setMaxLength(13)
        self.mailEdit.textChanged['QString'].connect(self._mail_check)
        self.mailEdit.setToolTip('输入您的邮箱')
        self.mailEdit.setMaxLength(21)
        # 检测验证码是否正确
        self.codeEdit.textChanged['QString'].connect(self._code_check)
        # 点击发送验证邮件按钮 调用send函数
        self.sendButton.clicked.connect(self._send)
        # 点击确认按钮，检验验证码，并上传至数据库，弹出通知栏关闭注册页面
        self.confirmButton.clicked.connect(self._update_userinfo)
        # 调用CloseDialog类中的close_signal 槽信号并绑定信号到self.close 既关闭RegisterForm这个类的方法
        self.success_dialog.close_signal.connect(self.close)

    def _mail_check(self):
        """
        检测邮件输入长度，太长则提示用户
        :param
        :return:
        """
        mail = self.mailEdit.text()
        if len(mail) > 20:
            self.mailStatus.setText("Too long")
        else:
            self.mailStatus.setText("Ok")

    def _newpassword_check(self):
        """
        检测密码输入长度，太长则提示用户
        :param
        :return:
        """
        newpassword = self.newpasswordEdit.text()
        if len(newpassword) > 12:
            self.newpasswordStatus.setText("Too long")
        else:
            self.newpasswordStatus.setText("Ok")

    def _code_check(self):
        """
        检测验证码是否正确，正确则更新self.flag，允许更新提交数据
        :param
        :return:
        """
        code = int(self.codeEdit.text())
        if code != self.verifyCode:
            self.codeStatus.setText("Wrong")

        else:
            # 确认用户邮箱
            self.flag = True
            print("Right verify code!")
            self.codeStatus.setText("Ok")

    def _send(self):
        """
        数据库查询用户输入邮箱是否存在
        实体化mailThread中的Mail类，开启发送邮件的线程
        开启线程执行self._count_down() 限制60秒内只能发送一发验证邮件
        :param
        :return:
        """
        # 获取用户输入的邮箱地址
        mailAddress = str(self.mailEdit.text())
        # 检测用户邮箱是否注册
        data_send = ['mail', mailAddress]
        mail_repeat = self.conn.search(TABLE_NAME, data_send)
        if mail_repeat is None:
            # 邮箱未注册
            print("邮箱未注册")
            self.mailStatus.setText("该邮箱未注册！")
        else:
            # 邮箱合法
            print("邮箱合法")
            self.id = mail_repeat[0][0]
            self.verifyCode = self._generate_code()
            print(self.senderMail + "   " + self.passwordMail + "verify code:" + str(self.verifyCode))
            send_thread = Mail(self.senderMail, self.passwordMail, mailAddress, self.verifyCode)
            # 用线程发送邮件 避免用户等待
            send_thread.start()
            # 用线程计时可重新发送邮件的等待时间 避免堵塞
            threading.Thread(target=self._count_down, args=()).start()

    def _count_down(self):
        """
        60秒倒计时，更新发送邮件按钮的文本
        :param
        :return:
        """
        # 按下按钮后过60s后才可以再次发送验证邮件
        current_time = 0
        # 禁用发送按钮
        self.sendButton.setEnabled(False)
        while current_time < 60:
            self.sendButton.setText(str(60 - current_time) + 's后可再发送')
            # 每过一秒更新一次时间
            time.sleep(1)
            current_time += 1
        # 60s后恢复发送按钮
        self.sendButton.setEnabled(True)
        self.sendButton.setText('发送验证邮件')

    def _generate_code(self):
        """
        生成验证码
        :param
        :return:
        """
        code = random.randint(100000, 999999)  # 生成六位随机数
        return code

    def _update_userinfo(self):
        """
        判断验证码是否正确
        更新用户数据，提交到数据库中
        显示实例化的CloseDialog类，提示用户注册完成，通过信号槽发送让RegisterForm类，即注册页面关闭的信号
        :param
        :return:
        """
        # 初始化封装在dataBase的连接
        mail_enter = str(self.mailEdit.text())
        newpassword_enter = str(self.newpasswordEdit.text())

        if self.flag:
            # 将用户信息添加到数据库
            data_send = [self.id, 'password', newpassword_enter]
            self.conn.edit(TABLE_NAME, data_send)
            self.success_dialog.show()
        else:
            self.codeStatus.setText("验证码错误，未收到邮件？")


TABLE_NAME = 'userinfo'
SERVER_ADDRESS = ('39.106.169.58', 3980)
if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化用于发送验证邮件的邮箱 以及STMP服务授权码

    conn = ConnectSQL(SERVER_ADDRESS)
    myWin = EditpasswordForm("614446871@qq.com", "rduygnlorlpgbeec", conn)
    # 将窗口控件显示在屏幕上
    myWin.show()

    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
