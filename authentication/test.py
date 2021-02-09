import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from authentication.dialogGUI import Biography



if __name__ == '__main__':
    app=QApplication(sys.argv)
    user_info = dict()
    user_info['name'] = '??'
    user_info['anime'] = 'Steins Gate'
    demo=Biography(user_info, 0,0)
    demo.show()
    sys.exit(app.exec_())
