# coding: utf-8
import struct


class Response(object):
    SOP1 = 0
    SOP2 = 1
    MRSP = 2
    SEQ = 3
    DLEN = 4

    CODE_OK = 0

    def __init__(self, header, data):
        self.header = header
        self.data = data

    @property
    def fmt(self):
        return '%sB' % len(self.data)

    def empty(self):
        return self.header[self.DLEN] == 1

    @property
    def success(self):
        return self.header[self.MRSP] == self.CODE_OK

    def seq(self):
        return self.header[self.SEQ]

    @property
    def body(self):
        return struct.unpack(self.fmt, self.data)

    def __str__(self):
        return str(self.header) + ',' + str(self.data)

class GetRGB(Response):
    def __init__(self, header, data):
        super(GetRGB, self).__init__(header, data)
        self.r = self.body[0]
        self.g = self.body[1]
        self.b = self.body[2]
        
    def __iter__(self):
        return iter((self.r,self.g,self.b))

    def __str__(self):
        return str(self.r) + ',' + str(self.g) + ',' + str(self.b)

class GetBluetoothInfo(Response):
    def __init__(self, header, body):
        super(GetBluetoothInfo, self).__init__(header, body)
        self.name = self.data.split('\x00', 1)[0]
        self.bta = self.data[16:].split('\x00', 1)[0]
