# coding: utf-8
'''串口测试数据生成器'''
from PyQt5.QtWidgets import QApplication
import sys
from datasender import DataSender

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DataSender()
    w.show()
    sys.exit(app.exec_())