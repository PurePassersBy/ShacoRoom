#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""悬停提示信息"""
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont
from authentication.dataBase import conn

if __name__ == '__main__':
    test = conn()
    test.insert("欧内的手好汉！","78124213@qq.com","sldjfklsdjf")