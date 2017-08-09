# coding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
import os
import sys

uipath, uiname = os.path.split(os.path.realpath(__file__))
uiname = uiname.replace('.py', '.ui')
uifile = os.path.join(uipath, uiname)
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class OptView(ui_mainwindow, qtbaseclass):
    '''操作界面'''

    def __init__(self, parent=None, name=None, value=None):
        super().__init__(parent)

        self.setupUi(self)
        self.label_name.setText(name)
        self.label_value.setText(value)

        self.setWindowFlags(QtCore.Qt.Dialog| QtCore.Qt.WindowTitleHint) # 弹出窗口，无边框




if __name__ == '__main__':
    app=QApplication(sys.argv)
    o=OptView(None,'name','value')
    o.show()
    sys.exit(app.exec_())