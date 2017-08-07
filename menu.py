# coding: utf-8
'''主菜单'''

from datalistview import DataListView
from submenu import SubMenu
from PyQt5 import QtWidgets, QtCore
from datamanager import MsgDataManager
from PyQt5 import QtSql
from login import UserLogin

PORT_NAME = 'com2'


class Menu(DataListView):
    msgManger = MsgDataManager(PORT_NAME)
    # 数据库相关
    model = QtSql.QSqlQueryModel()
    query = None

    # 用户信息
    user_info = {}

    def __init__(self):
        super().__init__()

        # 用户登录
        self.login()
        

        # 设置界面
        # self.setStyleSheet("background-color:#2C3E50;")
        # self.setWindowFlags(QtCore.Qt.Window)
        self.showFullScreen()

        self.setTableTitle('主菜单')
        self.setTableAutoStretch()
        # 设置显示模型
        self.setModel(self.model)

        # 关联接收事件处理
        self.msgManger.connectRead()

    def slot_fresh_pressed(self):
        win = SubMenu()
        # 关联数据更新
        self.msgManger.connectDataUpdate(win.slot_fresh_pressed)

        win.showDialog()

        # 子菜单窗口退出，断开数据更新
        self.msgManger.disconnectDataUpdate()

    def login(self):
        '''登录'''
        user = UserLogin()
        self.user_info[user.user] = user.pwd

    def slot_close_click(self):
        '''关闭'''
        self.login()

