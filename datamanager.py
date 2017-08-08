# coding: utf-8
from msgManager import MsgStruct, ComMsg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from datetime import datetime


class MsgDataManager(ComMsg):
    '''消息数据处理
    '''

    # 数据库接口
    db = QSqlDatabase.addDatabase('QSQLITE')

    SQL_TABLENAME = 'Topper'
    FMT_SQL_CREATE = '''create table if not exists {0} 
            (id integer primary key,
            devId varchar(10),
            code varchar(10),
            msg varchar(100),
            time varchar(100))'''
    # SQL 插入语句，0--表名称，1--列名称，2--列值
    FMT_SQL_INSERT = 'insert into {0} ({1}) values ({2})'

    FMT_SQL_UPDATE = 'update '
    SQL_DB_FILENAME = 'test.db'

    # 数据更新回调
    handler = None

    def __init__(self, portName):
        super(MsgDataManager, self).__init__(portName)
        self.db.setDatabaseName(':memory:')
        self.db.open()
        self.query = QSqlQuery()
        self.query.exec_(self.FMT_SQL_CREATE.format(self.SQL_TABLENAME))
        self.query.exec_('commit')

    def msgHandler(self, msg):
        '''数据处理详细过程'''
        msg.decode()
        msgId, devId, code, msgText = msg.toStringTuple()
        values = '{0},"{1}","{2}","{3}","{4}"'.format(msgId, devId, code,
                                                      msgText,
                                                      datetime.now().ctime())
        sql_insert = self.FMT_SQL_INSERT.format(
            self.SQL_TABLENAME, 'id,devId,code,msg,time', values)
        success = self.query.exec_(sql_insert)
        if success:
            self.query.exec_('commit')
            self.onDataUpdate()

    def connectRead(self):
        '''接收处理事件绑定'''

        # readyRead绑定到onRead
        self.serial.readyRead.connect(self.onRead)

    def onDataUpdate(self):
        '''数据更新回调'''

        # 如果回调接口为空直接退出
        if not self.handler:
            return
        try:
            self.handler()
        except Exception as e:
            print(e)

    def connectDataUpdate(self, handler):
        '''连接数据更新'''
        self.handler = handler

    def disconnectDataUpdate(self):
        '''取消连接数据更新'''
        self.handler = None


if __name__ == '__main__':
    mdm = MsgDataManager('COM1')
    mdm.wait()
