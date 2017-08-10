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

# QSS = '''
# QLabel{
#     color:black;
#     font-size:30px;
#     font-family:'宋体';
# }
# '''


class OptView(ui_mainwindow, qtbaseclass):
    '''操作界面'''
    value = ''
    check = False

    def __init__(self, parent=None, name=None, value=None):
        super().__init__(parent)

        self.setupUi(self)
        # self.setStyleSheet(QSS)

        self.label_name.setText(name)
        self.label_value.setText(value)
        self.value = value

        self.setWindowFlags(
            QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)  # 弹出窗口，无边框

    def slot_ok_clicked(self):
        '''确认点击'''
        value_edit = self.lineEdit.text()
        if value_edit.upper() == self.value.upper():
            self.check = True
            self.accept()
        else:
            self.check = False
            QMessageBox.critical(self, '错误', '值不匹配!')

    def slot_cancel_clicked(self):
        '''取消点击'''
        self.reject()

    def slot_enter_clicked(self):
        '''文本编辑回车键按下'''
        self.slot_ok_clicked()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    o = OptView(None, 'name', 'value')
    o.show()
    sys.exit(app.exec_())