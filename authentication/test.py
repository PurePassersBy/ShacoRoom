import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from authentication.dialogGUI import Biography
from authentication.connecter.SQLConn import ConnectSQL

SERVER_ADDRESS = ('39.106.169.58', 3980)
TABLE_NAME = 'userinfo'
if __name__ == '__main__':
    conn = ConnectSQL(SERVER_ADDRESS)

    conn.edit(TABLE_NAME, ['1','biography','sadfsfsdfdsfsfsfsf!'])

