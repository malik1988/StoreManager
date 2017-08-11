# coding: utf-8
'''子菜单'''

from datalistview import DataListView
from PyQt5 import QtSql

from optview import OptView


class SubMenu(DataListView):
    user = None  # 用户信息
    db = None  # 数据库

    SQL_SELECT = 'select id as 序号,devId as 设备ID,code as 编码,msg as 消息,time as 时间 from Topper'

    def __init__(self, parent=None, user=None, db=None):
        super().__init__(parent)
        self.setTableTitle('子菜单')
        model = QtSql.QSqlQueryModel()
        self.setModel(model)
        # 设置窗口样式
        # self.setWindowFlags(QtCore.Qt.Popup) # 弹出窗口，无边框
        self.showFullScreen()  # 全屏模式
        self.setTableAutoStretch()
        # 设置用户信息
        self.user = user
        # 设置数据库
        self.db = db
        # 数据更新显示
        self.update_data_view()

    def update_data_view(self):
        '''数据更新显示'''
        self.model.setQuery(self.SQL_SELECT, self.db)

    def slot_table_click(self, index):
        # col = index.column()
        row = index.row()
        name = str(self.model.index(row, 1).data())
        value = str(self.model.index(row, 2).data())
        if value:
            # 开始
            opt = OptView(self, name, value)
            opt.exec_()
            if opt.check:
                # 操作成功
                pass
