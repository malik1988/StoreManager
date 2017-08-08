#coding: utf-8
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel


class DBManager(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('e:/Project/sql/user.db')
        self.db.open()
        self.query = QSqlQuery()
        # self.insert()

    def create(self):
        str_create_table = 'create table if not exists users(id integer primary key,name varchar(20),password varchar(20),time real)'
        self.query.exec_(str_create_table)
        self.query.exec_('commit')

    def insert(self):
        str_insert = 'insert into users (id,name,password,time) values (5,"aa","1122333",122.202)'
        self.query.exec_(str_insert)
        self.query.exec_('commit')

    def getTableModel(self):
        model = QSqlTableModel()
        model.setTable('users')
        # model.setFilter('id=1')
        model.select()

        return model

    def getQueryModel(self, queryStr):
        model = QSqlQueryModel()
        model.setQuery(queryStr)
        return model

    def update(self, key=0, values=None):
        pass


from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
import os
import sys

uipath, uiname = os.path.split(os.path.realpath(__file__))
uiname = uiname.replace('.py', '.ui')
uifile = os.path.join(uipath, uiname)
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class DataListView(ui_mainwindow, qtbaseclass):
    # 数据模型
    model = None

    # header=('1','2','3','4')
    def __init__(self):
        ui_mainwindow.__init__(self)
        qtbaseclass.__init__(self)
        self.setupUi(self)

    def setTableAutoStretch(self):
        # 设置表格自动填充
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

    def setTableTitle(self, title):
        self.tableTitle.setText(title)

    def setTableReadOnly(self):
        '''设置数据表只读'''
        # 设置表格只读
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def setModel(self, model):
        self.tableView.setModel(model)

    def slot_table_click(self, index):
        '''表格点击事件处理
        - index 点击索引
        '''
        pass

    def setLogoLeft(self, imgPath):
        img = QtGui.QImage(imgPath)
        icon = img.scaled(50, 50)
        pix = QtGui.QPixmap()
        self.logo_left.setPixmap(pix.fromImage(icon))

    def setLogoRight(self, imgPath):
        img = QtGui.QImage(imgPath)
        icon = img.scaled(50, 50)
        pix = QtGui.QPixmap()
        self.logo_right.setPixmap(pix.fromImage(icon))

    def slot_fresh_pressed(self):
        '''refresh'''
        pass

    def slot_close_click(self):
        '''关闭按钮点击事件'''
        self.reject()


if __name__ == '__main__':
    # d = DBManager()
    # d.create()
    app = QApplication(sys.argv)
    w = DataListView()
    w.setTableTitle('数据显示')
    w.show()
    sys.exit(app.exec_())
