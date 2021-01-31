# -*- coding: utf-8 -*-
import sys
import random
import time

import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore

sys.path.append('..')

from mailThread import Mail
from verifyGUI import Ui_Verify
from loginGUI import Ui_login
from dialogGUI import Ui_Dialog
from DAO.dataBase import ConnectSQL
from gui.ChatGui import ChatGUI



SERVER_ADDRESS = ('39.106.169.58', 3980)
TABLE_NAME = 'userinfo'

class RegisterForm(QMainWindow, Ui_Verify):
    def __init__(self, senderMail, passwordMail, conn):
        """
        初始化RegisterForm类，设置不同按钮连接的槽与信号函数，实例化注册完成通知类CloseDialog()以便完成信号槽连接
        :param senderMail:   发送邮箱
        :param passwordMail:    stmp授权码
        :return:
        """
        super(RegisterForm, self).__init__()
        # 实例化子类dialog,这一步一定要在self.initUi前面,不然initUi中不能调用没有实例化的close_signal这个槽信
        self.success_dialog = CloseDialog()
        self.setupUi(self)
        self.retranslateUi(self)
        # 接收来自登陆界面的DAO connect
        self.conn = conn
        # 储存发送邮箱以及邮箱stmp授权码
        self.senderMail = senderMail
        self.passwordMail = passwordMail
        # 验证码是否正确的标志
        self.flag = False
        # 储存生存的验证码
        self.verifyCode = None
        # 添加检测文本变化信号和槽 设置长度限制提示  设置最大输入字符数
        self.nameEdit.textChanged['QString'].connect(self._name_check)
        self.nameEdit.setToolTip('长度不超过8')
        self.nameEdit.setMaxLength(9)
        self.passwordEdit.textChanged['QString'].connect(self._password_check)
        self.passwordEdit.setToolTip('长度不超过12')
        self.passwordEdit.setMaxLength(13)
        self.mailEdit.textChanged['QString'].connect(self._mail_check)
        self.nameEdit.setToolTip('输入您的邮箱')
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

    def _name_check(self):
        """
        检测用户名输入长度，太长则提示用户
        :param
        :return:
        """
        name = self.nameEdit.text()
        if len(name) > 8:
            self.nameStatus.setText("Too long")
        else:
            self.nameStatus.setText("Ok")

    def _password_check(self):
        """
        检测密码输入长度，太长则提示用户
        :param
        :return:
        """
        password = self.passwordEdit.text()
        if len(password) > 12:
            self.passwordStatus.setText("Too long")
        else:
            self.passwordStatus.setText("Ok")

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
            # 邮箱合法
            print("邮箱合法")
            self.verifyCode = self._generate_code()
            print(self.senderMail + "   " + self.passwordMail + "verify code:" + str(self.verifyCode))
            send_thread = Mail(self.senderMail, self.passwordMail, mailAddress, self.verifyCode)
            # 用线程发送邮件 避免用户等待
            send_thread.start()
            # 用线程计时可重新发送邮件的等待时间 避免堵塞
            threading.Thread(target=self._count_down, args=()).start()
        else:
            # 邮箱重复
            print("邮箱重复")
            self.mailStatus.setText("该邮箱已被注册！")

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
            self.sendButton.setText(str(60-current_time)+'s后可再发送')
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
        name_enter = str(self.nameEdit.text())
        password_enter = str(self.passwordEdit.text())

        if self.flag:

            # 将用户信息添加到数据库
            data_send = [name_enter, mail_enter, password_enter]
            self.conn.insert(TABLE_NAME, data_send)
            self.success_dialog.show()

        else:
            self.codeStatus.setText("未收到邮件？请检查邮箱是否输入错误")
            pass


class CloseDialog(QMainWindow, Ui_Dialog):
    # pyqtSignal 要定义为一个类而不是属性，不能放到__init__里
    close_signal = QtCore.pyqtSignal()

    def __init__(self):
        """
        注意close_signal 要在类成员函数外定义
        初始化CloseDialog类，将 确定 和 取消 按钮连接到self._close函数
        :param
        :return:
        """
        super(CloseDialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        self.buttonBox.accepted.connect(self._close)
        self.buttonBox.rejected.connect(self._close)

    def _close(self):
        """
        发送关闭信号给RegisterForm类，即关闭注册GUI
        同时关闭CloseDialog类，即关闭本窗口
        :param
        :return:
        """
        self.close_signal.emit()
        self.close()




class LoginForm(QMainWindow, Ui_login):
    def __init__(self):
        """
        初始化LoginForm类，设置不同按钮连接的槽与信号函数
        实例化RegisterForm()类以便完成显示注册界面，并输入注册发送邮件的邮箱与stmp授权码
        :param:
        :return:
        """
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.mail = None
        self.password = None
        # 初始化操作数据库的Connect
        self.conn = ConnectSQL(SERVER_ADDRESS)
        # 添加检测验证码文本变化信号和槽 mil password主要检测长度
        self.mailEdit.textChanged['QString'].connect(self._mail_check)
        self.mailEdit.setToolTip('没有邮箱？请先注册')
        self.mailEdit.setMaxLength(21)

        self.passwordEdit.textChanged['QString'].connect(self._password_check)
        self.passwordEdit.setToolTip('长度不超过12')
        self.passwordEdit.setMaxLength(13)
        # 点击发送验证邮件按钮 调用send函数
        self.loginButton.clicked.connect(self._login)
        self.registerButton.clicked.connect(self._register)
        # 初始化注册界面
        self.qt_register = RegisterForm("614446871@qq.com", "rduygnlorlpgbeec", self.conn)
        # 初始化聊天室界面
        self.qt_chat = None
    def _mail_check(self):
        """
        检测邮箱输入长度，太长则改变文本提示用户
        :param:
        :return:
        """
        mail = str(self.mailEdit.text())
        length = len(mail)
        if length > 20:
            self.mailStatus.setText('Too long')
        else:
            self.mailStatus.setText('Oook')

    def _password_check(self):
        """
        检测密码输入长度，太长则改变文本提示用户
        :param:
        :return:
        """
        password = str(self.passwordEdit.text())
        if len(password) > 12:
            self.passwordStatus.setText('Too long')
        else:
            self.passwordStatus.setText('Oook')

    def _login(self):
        """
        确认按钮连接的槽函数
        向数据库发送查询邮箱的请求，获得相应用户数据
        检测用户输入邮箱是否存在对应账号，以及密码是否匹配
        连接聊天室节面（待对接）
        :param:
        :return:
        """
        self.mail = str(self.mailEdit.text())
        self.password = str(self.passwordEdit.text())
        # 向服务器发送sql查询请求
        send_data = ['mail', self.mail]
        result = self.conn.search(TABLE_NAME, send_data)
        if result is None:
            self.mailStatus.setText('该邮箱未注册，请先注册')
        else:
            # result 返回的是一个二维tuple
            if result[0][3] == self.password:
                self.passwordStatus.setText('密码正确')
                # 接入聊天室
                self.qt_chat = ChatGUI(
                    result[0][0], result[0][1], 'Stein Gates', True, self.conn)
                self.qt_chat.show()
                self.close()
            else:
                self.passwordStatus.setText('密码错误')


    def _register(self):
        """
        注册按钮跳转至注册界面的槽函数
        :param:
        :return:
        """
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
