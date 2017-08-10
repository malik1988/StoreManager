#coding: utf-8
# python3 qt5
# 登录界面
'''用户登录界面
# 现有功能说明
- 用户名和密码输入并验证
- 禁用窗口关闭功能
'''

from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QMessageBox
from PyQt5 import QtCore
from PyQt5 import uic
import os
import sys
ui_file = os.path.split(os.path.realpath(__file__))[0] + '/login.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_file)


class Login(Ui_MainWindow, QtBaseClass):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog| QtCore.Qt.WindowTitleHint) # 弹出窗口，无边框
        # self.showFullScreen() # 全屏模式

        self.user = None  # 用户名
        self.pwd = None  # 密码
        self.ok = False

        self.exec_()

    def login(self):
        '''重构login方法
        ui中将login与lineEdit_pwd.returnPressed关联
        '''
        user = self.lineEdit_user.text()
        pwd = self.lineEdit_pwd.text()
        if user and pwd:
            # 用户名和密码同时不为空
            if self.check(user, pwd):
                # 登录成功，调用accept退出界面
                self.accept()
                self.ok = True
            else:
                QMessageBox.critical(self, '错误', '用户名或密码有误！')
        else:
            QMessageBox.critical(self, '错误', '用户名或密码不能为空！')

    def check(self, user, pwd):
        '''检查是否登录成功
        # user 
        用户名
        # pwd 
        用户密码
        # return 
        返回True/False表示成功失败
        '''
        self.user = user
        self.pwd = pwd
        return False

    def closeEvent(self, event):
        '''窗口关闭事件'''
        QMessageBox.warning(self, '警告', '请等登录')
        event.ignore()  # 忽略关闭，继续运行


class UserLogin(Login):
    def check(self, user, pwd):
        '''重写用户验证'''
        if user == pwd:
            self.user = user
            self.pwd = pwd
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Login()
    d.show()
    sys.exit(app.exec_())