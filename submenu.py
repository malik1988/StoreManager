# coding: utf-8
'''子菜单'''

from datalistview import DataListView
from PyQt5 import QtSql


class SubMenu(DataListView):
    model = QtSql.QSqlQueryModel()
    user = None  # 用户信息
    db = None  # 数据库

    SQL_SELECT = 'select id as 序号,msg as 消息,time as 时间 from Topper'

    def __init__(self, user=None, db=None):
        super().__init__()
        self.setTableTitle('子菜单')
        self.setModel(self.model)
        # 设置窗口样式
        # self.setWindowFlags(QtCore.Qt.Popup) # 弹出窗口，无边框
        self.showFullScreen()  # 全屏模式
        self.setTableAutoStretch()
        # 设置用户信息
        self.user = user
        # 设置数据库
        self.db = db
        # 数据更新显示
        self.model.setQuery(self.SQL_SELECT, self.db)

    def update_data_view(self):
        '''数据更新显示'''
        self.model.setQuery(self.SQL_SELECT, self.db)

    def slot_table_click(self, index):
        col = index.column()
        row = index.row()
        value = str(self.model.index(row, col).data())
        if value == 'start':
            # 开始
            pass
