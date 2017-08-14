# coding: utf-8
'''消息管理
- 串口数据传输
- 串口协议解析
'''

from PyQt5 import QtSerialPort, QtCore
import time
import struct
import binascii

MIN_LEN = 9


class MsgStruct(object):
    # 消息ID（bytes类型），固定长度2字节
    msgId = None
    # 设备ID（bytes类型），固定长度2字节
    devId = None
    # 消息功能码（bytes类型），固定长度1字节
    code = None
    # 消息内容（bytes类型），可变长度
    msg = None

    # 消息源码（bytes类型）
    data = None

    def __init__(self,
                 data=None,
                 length=0,
                 msgId=None,
                 devId=None,
                 code=None,
                 msg=None):
        if data and length:
            self.data = data[:length]
        self.msgId = msgId
        self.devId = devId
        self.code = code
        self.msg = msg

    def decode(self):
        '''数据解析'''
        if self.data and len(self.data) >= MIN_LEN:
            index = 3  # 直接跳过包头和长度，共3个字节
            self.msgId = self.data[index:index + 2]
            index += 2
            self.devId = self.data[index:index + 2]
            index += 2
            self.code = self.data[index:index + 1]
            index += 1
            self.msg = self.data[index:-1]

    def encode(self, msgId, devId, msg):
        '''数据打包
        - msgId 消息ID（十进制string）
        - devId 设备ID (十六进string)
        - msg 消息内容（utf-8字符串）
        '''
        # 包头2字节，长度1字节
        length = 3
        data = None

        # 消息ID，十进制数(0~65535)
        msgId = int(msgId)
        length += 2
        # 设备ID，十六进制数（0000~FFFF）
        devId = int(devId, 16)
        length += 2
        # 消息内容，ASCII字符串(最大长度255-9=246)
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

        self.data = data_bytes + check_byte
        return self.data

    def getCheckByte(self, data):
        sum = 0
        for b in data[:-1]:
            sum ^= b
        return sum

    def check(self):
        '''数据校验'''
        if self.getCheckByte(self.data) == self.data[len(self.data) - 1]:
            return True
        else:
            return False

    def bytes2hexStr(self, bytesData):
        strData = ''
        if bytesData:
            for x in bytesData:
                strData += hex(x).replace('0x', '').upper()
        return strData

    def toStringTuple(self):
        '''将MsgStruct成员转成字符串型数据（返回一个tuple）
        - return
            (msgId,devId,code,msg)
        '''
        strMsgId = ''
        strDevId = ''
        strCode = ''
        strMsg = ''
        if self.msgId:
            # 高字节在前
            iMsgId = struct.unpack('>H', self.msgId)
            strMsgId = str(iMsgId[0])

        if self.devId:
            # 高字节在前
            iDevId = struct.unpack('>H', self.devId)
            strDevId = str(iDevId[0])
        if self.code:
            iCode = struct.unpack('B', self.code)
            strCode = str(iCode[0])
        if self.msg:
            # strMsg = self.bytes2hexStr(self.msg)
            strMsg = str(self.msg, encoding='utf-8')

        return (strMsgId, strDevId, strCode, strMsg)


class SerialReciver(QtCore.QThread):
    '''接收线程
    - parent 线程父节点
    - fun 线程运行回调
    '''
    def __init__(self, parent=None, fun=None):
        super().__init__(parent)
        self.__func = fun

    def run(self):
        if self.__func:
            self.__func()


class ComMsg(QtCore.QObject):
    # 串口设备
    serial = QtSerialPort.QSerialPort()
    # 是否打开标志
    isOpen = False
    # 接收线程
    thread = None

    def __init__(self, portName):
        super().__init__()
        valid = False
        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            print('Debug: Avilable Com :%s' % info.portName())
            if portName.upper() == info.portName().upper():
                valid = True
                self.serial.setPort(info)
                break

        if valid:  # 存在该端口号
            self.serial.setBaudRate(self.serial.Baud115200)
            self.serial.setParity(self.serial.NoParity)
            self.serial.setDataBits(self.serial.Data8)
            self.serial.setStopBits(self.serial.OneStop)

            # self.serial.readyRead.connect(self.onRead)
            self.serial.open(QtCore.QIODevice.ReadWrite)
            if self.serial.isOpen():
                self.isOpen = True
                # 设备打开创建线程
                self.thread = SerialReciver(self, self.wait)
                # 运行线程
                self.thread.start()
            else:
                print('Debug: Com %s Open Failed' % self.serial.portName())

        else:
            print('%s is Not Valid' % portName)

    def onRead(self):
        '''数据接收'''
        buf = self.serial.readAll()
        # 获取bytes类型的数据进行下一步处理
        buf = buf.data()
        print('Debug: Got Data %r' % buf)
        while len(buf) >= MIN_LEN:
            if buf[0] == 0xaa and buf[1] == 0x55:  # 找到头
                # 获取长度
                length = buf[2]

                if len(buf) < int(length):
                    break  # 长度不够直接退出
                msg = MsgStruct(buf, length)

                if not msg.check():
                    # 删除包头的长度，2字节
                    buf = buf[2:]
                    continue

                # 这里开始表明接收到有效的数据包
                # 开始做具体的数据处理

                # msg.decode()
                # t = msg.toStringTuple()
                # TODO 数据处理
                self.msgHandler(msg)

                # 删除处理完的数据
                buf = buf[length:]

            else:
                # 跳过第一个字节
                buf = buf[1:]

    def wait(self):
        '''死等接收数据'''
        while True:
            if self.serial.waitForReadyRead(1000):
                # data = self.serial.readAll()
                self.onRead()
                # print(data, 'at time %s' % time.ctime())
            else:
                print('timeout at %s' % (time.ctime()))

    def msgHandler(self, msg):
        '''消息数据处理回调函数接口（根据需要自己实现）'''
        pass



def main():
    c = ComMsg('com1')
    c.wait()


if __name__ == '__main__':
    main()