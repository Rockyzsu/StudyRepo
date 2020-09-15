#！/usr/bin/python
#coding:utf-8

import time
import gevent
from gevent import select

start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)

def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('Started 1 Polling: ', tic())
    select.select([], [], [], 2) # 类似与gevent.sleep()
    print('Ended Polling: ', tic())

def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('Started 2 Polling: ', tic())
    select.select([], [], [], 2)
    print('Ended Polling: ', tic())

def gr3():
    print("Hey lets do some stuff while the greenlets poll, at", tic())
    gevent.sleep(1)
    print('gre3 is done: ', tic())

gevent.joinall([
    gevent.spawn(gr1),
    gevent.spawn(gr2),
    gevent.spawn(gr3),
])
