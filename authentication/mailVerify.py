# -*- coding: UTF-8 -*-
import smtplib
import socket
import threading
import random
import time
from email.mime.text import MIMEText
from email.utils import formataddr

class Mail():
    def __init__(self, sender, password, receiver):
        # 第三方SMTP服务
        self.mailSender = sender
        self.mailPassword = password
        self.mailReceiver = receiver
        self.verifyCode
    def send(self):
        self.verifyCode = self.generateCode()
        flag = True
        try:
            msg = MIMEText('欢迎注册ShacoRoom 您的验证码为：' + str(self.verifyCode) + '\n请在十五分钟内完成验证', 'plain', 'utf-8')      #邮件内容
            msg['From'] = formataddr(["ShacoRoom", self.mailSender])            # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["Dear ShacoRoom User", self.mailReceiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "ShacoRoom注册验证码"                               # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)                       # 发件人邮箱中的SMTP服务器，qqmail端口是465
            server.login(self.mailSender, self.mailPassword)                    # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.mailSender, [self.mailReceiver,], msg.as_string())
            server.quit()                                                       # 关闭连接
        except Exception:
            flag = False
        return flag

    def generateCode(self):
        code = random.randint(100000, 999999)                                   #生成六位随机数
        return code

