# coding: utf-8

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtSerialPort
from PyQt5 import uic
import os
import sys
import struct
import binascii

uipath, uiname = os.path.split(os.path.realpath(__file__))
uiname = uiname.replace('.py', '.ui')
uifile = os.path.join(uipath, uiname)
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class DataSender(ui_mainwindow, qtbaseclass):
    '''串口数据发送显示界面'''

    serial = QtSerialPort.QSerialPort()

    def __init__(self):

        ui_mainwindow.__init__(self)
        qtbaseclass.__init__(self)
        self.setupUi(self)

        port_list = []

        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            port_list.append(info.portName())

        if port_list:
            self.comboBox_port.addItems(port_list)

        self.serial.readyRead.connect(self.onRead)

        
    def onRead(self):
        '''数据接收并显示'''
        data=self.serial.readAll()
        # str_data=binascii.unhexlify(data)
        str_data=str(data)

        
        self.textBrowser.setPlainText(str_data)


    def build_data(self):
        '''产生数据
        - return
        bytes型数据'''

        # 包头2字节，长度1字节
        length = 3
        data = None

        # 消息ID，十进制数(0~65535)
        msgId = self.lineEdit_msgId.text()
        msgId = int(msgId)
        length += 2
        # 设备ID，十六进制数（0000~FFFF）
        devId = self.lineEdit_devId.text()
        devId = int(devId, 16)
        length += 2
        # 消息内容，ASCII字符串(最大长度255-9=246)
        msg = self.textEdit_msg.toPlainText()
        msg = bytes(msg, encoding='utf-8')
        length += len(msg)
        str_pack = '!BBBHH{0}s'.format(len(msg))

        # 加上校验字节长度
        length += 1

        data = struct.Struct(str_pack)
        # 包头两个字节AA55,长度，消息ID，设备ID，消息内容
        value = (0xAA, 0x55, length, msgId, devId, msg)

        data_bytes = data.pack(*value)
        check = self.getCheckByte(data_bytes)

        # 填充校验字节

        check_pack = struct.Struct('B')
        check_value = (check, )
        check_byte = check_pack.pack(*check_value)

        return data_bytes + check_byte

    def getCheckByte(self, data):
        sum = 0
        for b in data:
            sum ^= b
        return sum

    def slot_send_click(self):
        '''发送按钮点击事件'''
        if not self.serial.isOpen():
            return

        data = self.build_data()

        try:
            ret = self.serial.writeData(data)
        except Exception as e:
            print(e)

    def slot_port_change(self, text):
        '''端口号改变事件'''
        if not self.serial.isOpen():
            self.serial.setPortName(text)

    def slot_connect_click(self):
        '''连接设备'''
        if not self.serial.isOpen():
            self.serial.setBaudRate(self.serial.Baud115200)
            self.serial.setParity(self.serial.NoParity)
            self.serial.setDataBits(self.serial.Data8)
            self.serial.setStopBits(self.serial.OneStop)

            try:
                self.serial.open(QtCore.QIODevice.ReadWrite)
            except Exception as e:
                print(e)
                return
        else:
            self.serial.close()

        if self.serial.isOpen():
            self.pushButton_connect.setText('关闭连接')
            self.comboBox_port.setEnabled(False)
            QMessageBox.warning(self,'警告','设备已经打开！')
        else:
            self.pushButton_connect.setText('打开连接')
            self.comboBox_port.setEnabled(True)
            QMessageBox.warning(self,'警告','设备关闭！')
