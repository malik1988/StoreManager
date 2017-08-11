# coding: utf-8
'''主菜单'''

from datalistview import DataListView
from submenu import SubMenu
from PyQt5 import QtWidgets, QtGui, QtCore
from datamanager import MsgDataManager
from login import UserLogin

import config


class Menu(DataListView):
    msgManger = MsgDataManager(config.APP_COM_NAME)
    # 数据库相关
    # model = QtSql.QSqlQueryModel()
    # query = None

    # 用户信息
    isLogin = False
    user_info = {}

    def __init__(self):
        super().__init__()

        # 用户登录
        self.login()

        # 设置界面
        # self.setWindowFlags(QtCore.Qt.Window)
        self.showFullScreen()

        self.setTableTitle('主菜单')
        self.setTableAutoStretch()
        # 设置显示模
        model = QtGui.QStandardItemModel()
        headers = ('编号', '名称', '动作')
        model.setHorizontalHeaderLabels(headers)
        values = ('name1', 'name2', 'name3')
        for i, x in enumerate(values):
            model.setItem(i, 0, QtGui.QStandardItem(str(i)))
            model.setItem(i, 1, QtGui.QStandardItem(x))
            model.setItem(i, 2, QtGui.QStandardItem('start'))

        self.setModel(model)
        self.setTableReadOnly()

        # 关联接收事件处理
        self.msgManger.connectRead()

    def show_sub_menu(self):
        '''显示子菜单'''
        self.setVisible(False)
        win = SubMenu(parent=self, user=self.user_info, db=self.msgManger.db)
        # 关联数据更新
        self.msgManger.connectDataUpdate(win.update_data_view)
        win.exec_()

        # 子菜单窗口退出，断开数据更新
        self.msgManger.disconnectDataUpdate()
        self.setVisible(True)
        self.showFullScreen()

    def login(self):
        '''登录'''
        if not self.isLogin:
            user = UserLogin(self)
            self.user_info[user.user] = user.pwd
            self.isLogin = True
            self.setVisible(True)

    def slot_close_click(self):
        '''关闭'''
        self.setVisible(False)
        self.isLogin = False

        self.login()

    def slot_table_click(self, index):
        col = index.column()
        row = index.row()
        value = str(self.model.index(row, col).data())

        if value == 'start':
            self.show_sub_menu()
