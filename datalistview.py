#coding: utf-8

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
import os
import sys

uipath, uiname = os.path.split(os.path.realpath(__file__))
uiname = uiname.replace('.py', '.ui')
uifile = os.path.join(uipath, uiname)
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)
'''
C07010 橙色
'''

QSS = '''
QDialog{
    background-color:#DAA520;
}
QPushButton
{
    background-color:#FF8C00;
    color:#000000;
    border-width:2px;
    border-style:solid;
    border-radius:5px;
}

QTableView{  
    color: rgb(0, 0, 0);  
    border: 1px solid #C07010;          /*边框颜色*/  
    gridline-color:#C07010;             /*grid线颜色*/  
    background-color:#DAA520;  //背景橙色
    alternate-background-color: rgb(200, 200, 200); /*行交替颜色*/  
    selection-background-color: rgb(130, 190, 100); /*选中行背景颜色*/  
}  
  
QTableView::item:!alternate:!selected{  
    background-color: rgb(220, 220, 220);    /*交替行的另一颜色*/  
}  
QHeaderView::section{  
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(80, 80, 80, 255), stop:1 rgba(30, 30, 30, 255));  
    color: rgb(240, 240, 240);  
    padding-left: 4px;  
    border: 1px solid #C07010;  
    min-height: 50px;  
    font-size:36px;
} 
'''


class DataListView(ui_mainwindow, qtbaseclass):
    # 数据模型
    model = None

    # header=('1','2','3','4')
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(QSS)

    def setTableAutoStretch(self):
        # 设置表格自动填充
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        # self.tableView.verticalHeader().setDefaultSectionSize(50)
        # self.tableView.verticalHeader().hide()

    def setTableTitle(self, title):
        self.tableTitle.setText(title)

    def setTableReadOnly(self):
        '''设置数据表只读'''
        # 设置表格只读
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def setModel(self, model):
        self.model = model
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
