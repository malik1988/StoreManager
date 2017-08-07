#coding: utf-8
# 主程序入口
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox,QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic
from login import UserLogin
from datalistview import DataListView, DBManager

from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase
from datamanager import MsgDataManager

# # remote debug
# import ptvsd
# address = ('0.0.0.0', 8000)
# ptvsd.enable_attach('my_secret', address)
# ptvsd.wait_for_attach()
# # ptvsd.settrace('my_secret', address=address)
# print('Remote Debug Connect')


class Store(DataListView):

    mdm = MsgDataManager('COM2')
    model = QSqlQueryModel()
    query = None
    user_info = {}

    def __init__(self):
        super(Store, self).__init__()
        # 用户登录
        user = UserLogin()
        self.user_info[user.user] = user.pwd

        self.setTableTitle('数据查询')
        self.setTableAutoStretch()
        self.setLogoLeft('E:/Project/PyQt/Store/data.ico')
        self.setLogoRight('E:/Project/PyQt/Store/mars.ico')
        # 设置显示模型
        self.setModel(self.model)

        # 绑定数据读取事件
        self.mdm.connectRead()
        # 绑定数据更新事件
        self.mdm.connectDataUpdate(self.slot_fresh_pressed)

    def slot_table_click(self, index):
        col = index.column()
        row = index.row()
        value = str(self.model.index(row, col).data())

    def init_DataBase(self):
        '''初始化数据库'''
        str_select = '''select * from message'''
        self.model.setQuery(str_select)

    def slot_fresh_pressed(self):
        '''数据更新'''
        str_select = '''select * from message'''
        self.model.setQuery(str_select, self.mdm.db)


from menu import Menu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = Menu()
    l.show()
    sys.exit(app.exec_())