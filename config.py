# coding: utf-8
'''配置文件
'''
import os
import platform

# APP所在目录
APP_DIR = os.path.split(os.path.realpath(__file__))[0]

# 数据库名
# 内存方式：APP_DB_NAME=':memory:'
APP_DB_NAME = os.path.join(APP_DIR, 'test.db')

# 左右图标名
APP_ICO_LEFT = 'data.ico'
APP_ICO_RIGHT = 'mars.ico'

# 主界面的大小
APP_SIZE_WIDTH = 1024
APP_SIZE_HEIGHT = 600

# 串口设备名称
# Linux系统COM名设置： APP_COM_NAME='ttyS0'
if platform.system() == 'Linux':
    APP_COM_NAME = 'ttyS0'
else:
    APP_COM_NAME = 'com2'
