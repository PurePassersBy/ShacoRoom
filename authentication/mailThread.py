# -*- coding: UTF-8 -*-
import threading

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail(threading.Thread):
    # 继承线程，完成邮件发送
    def __init__(self, sender, password, receiver, verify_code):
        """
        发送邮件
        :param sender:      发送邮箱
        :param password:    stmp授权码
        :param receiver:    接收邮箱
        :param verify_code: 验证码
        :return:Void:
        """
        # 第三方SMTP服务
        super(Mail, self).__init__()
        self.mailSender = sender
        self.mailPassword = password
        self.mailReceiver = receiver
        # 生成6位随机验证码
        self.verifyCode = verify_code
        # sendResult初始状态，线程结束后更新状态为True 或者False
        self.sendResult = None


    def run(self):
        """
        发送邮件
        :param：
        :return:
        """
        try:
            msg = MIMEText('欢迎注册ShacoRoom 您的验证码为：' + str(self.verifyCode) + '\n请在十五分钟内完成验证', 'plain', 'utf-8')  # 邮件内容
            msg['From'] = formataddr(["ShacoRoom", self.mailSender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["Dear ShacoRoom User", self.mailReceiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "ShacoRoom注册验证码"  # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，qqmail端口是465
            server.login(self.mailSender, self.mailPassword)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.mailSender, [self.mailReceiver, ], msg.as_string())
            print("Send successfully")
            self.sendResult = True  # 邮件发送成功的flag
            server.quit()  # 关闭连接
        except Exception:
            print("Send failed")
            self.sendResult = False #邮件发送失败




