#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

# 子类化Greenlet类，重载_run方法

import gevent
from gevent import Greenlet

class MyGreenlet(Greenlet):

    def __init__(self, message, n):
        Greenlet.__init__(self)
        self.message = message
        self.n = n

    def _run(self):
        print(self.message)
        gevent.sleep(self.n)

g = MyGreenlet("Hi there!", 1)
g.start()
g.join()