# coding: utf-8
'''子菜单'''

from datalistview import DataListView, DBManager
from PyQt5 import QtSql,QtCore
class SubMenu(DataListView):
    model=QtSql.QSqlQueryModel()
    def __init__(self):
        super().__init__()
        self.setTableTitle('子菜单')
        self.setModel(self.model)
        # 设置窗口样式
        # self.setWindowFlags(QtCore.Qt.Popup) # 弹出窗口，无边框
        self.showFullScreen() # 全屏模式


    def slot_fresh_pressed(self):
        # self.model.setQuery('select * from message',self.)
        print('gotdata')

    def showDialog(self):
        '''显示对话框(阻塞方式)'''
        self.exec_()

