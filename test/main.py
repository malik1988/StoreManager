# coding: utf-8
from PyQt5.QtWidgets import QApplication
import sys
from  datasender import DataSender

import structfmt


s=(structfmt.struct_named_format('name')
.network_endian()
.uint8('header1','header2')
.uint8('length')
.uint16('msgId')
.uint16('devId')
.uint8('msg')
.uint8('crc')
).build_formatted_struct()

packed=s.pack(0xaa,0x55,0x09,0x0001,0x001f,0,0x1f)
print(packed)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DataSender()
    w.show()
    sys.exit(app.exec_())