# coding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
import os
import sys
import config

uifile = os.path.join(config.APP_DIR, 'optview.ui')
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class OptView(ui_mainwindow, qtbaseclass):
    '''操作界面'''
    value = ''
    check = False

    def __init__(self, parent=None, name=None, value=None):
        super().__init__(parent)

        self.setupUi(self)
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
            # 清空文本框，等待下次输入
            self.lineEdit.setText('')
            QMessageBox.critical(self, '错误', '值不匹配!')

    def slot_cancel_clicked(self):
        '''取消点击'''
        self.reject()

    def slot_enter_clicked(self):
        '''文本编辑回车键按下'''
        self.slot_ok_clicked()

    def keyPressEvent(self, event):
        '''重写键盘响应事件'''
        if event.key() == QtCore.Qt.Key_Escape:
            # 不处理ESC按键
            pass
        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    o = OptView(None, 'name', 'value')
    o.show()
    sys.exit(app.exec_())