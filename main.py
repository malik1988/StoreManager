#coding: utf-8
# 主程序入口
import sys
from PyQt5.QtWidgets import QApplication
from menu import Menu

QSS = '''
QDialog,QWindow{
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
    background-color:#DAA520;  
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    l = Menu()
    l.show()
    sys.exit(app.exec_())