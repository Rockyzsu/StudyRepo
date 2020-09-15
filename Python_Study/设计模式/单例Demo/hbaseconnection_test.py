# -*- coding: utf-8 -*-
# @Time    : 2017/7/31 14:15
# @Author  : 哎哟卧槽
# @Site    : 
# @File    : hbaseconnection.py
# @Software: PyCharm
import sys
import happybase
from happybase import NoConnectionsAvailable
from datetime import datetime
from common.public import *
import threading
Lock = threading.Lock()

sys.setrecursionlimit(1500)


class HappyBaseConnection(object):

    __instance = None

    # def __init__(self, host='localhost', port=9090, *args, **kwargs):
    #     self.HB = happybase.Connection(host=host, port=port)
    #     self.HB.open()
    #     print('打开连接', self.HB)

    def __new__(cls, host='localhost', port=9090, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(HappyBaseConnection, cls).__new__(cls, *args, **kwargs)
                    hb = happybase.Connection(host=host, port=port)
                    hb.open()
                    setattr(cls.__instance, 'hb', hb)
                    print('我只会调用一次')
            finally:
                Lock.release()
        return cls.__instance

    def puts(self, table_name, row_key, mutations, send):
        table = self.hb.table(table_name)
        try:
            with table.batch(transaction=True) as b:
                if send:
                    b.put(row_key, mutations)
                    b.send()
                    print('处理任务结束：', datetime.now())
                    return True
                else:
                    b.put(row_key, mutations)
        except NoConnectionsAvailable as err:
            print(err.args)
            raise NoConnectionsAvailable

    def get_data(self, table_name, row_key, columns):
        print('开始查询数据：', datetime.now())
        table = self.hb.table(table_name)
        if not isinstance(columns, list):
            raise ValueError ("{}参数必须是list".format(columns))
        columns = [conve_byte(i) for i in columns]
        row = table.row(conve_byte(row_key), columns=columns)
        return row


if __name__ == '__main__':
    HB = HappyBaseConnection('10.10.1.246')
    HB2 = HappyBaseConnection('10.10.1.246')
    print(HB)
    print(HB2)
    print(HB.get_data('webpages', '00117ee05a64db33ed3ad5bde3c58bfc', ['spider:info']))
    # print(HB.get_data('webpages', '00117ee05a64db33ed3ad5bde3c58bfc'))
    print('查询数据结束:', datetime.now())