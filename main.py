#coding: utf-8
# 主程序入口
import sys
from PyQt5.QtWidgets import QApplication
from menu import Menu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = Menu()
    l.show()
    sys.exit(app.exec_())