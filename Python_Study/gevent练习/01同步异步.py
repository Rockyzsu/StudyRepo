#！/usr/bin/python
#coding:utf-8
# Done

import time
import gevent
import requests
def foo():
    print('Running in foo')
    # time.sleep(2) # 这样子不起作用
    gevent.sleep(2) # 通过它各自yield向对方
    # r=requests.get('http://30daydo.com')
    # print(r.status_code)
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    # time.sleep(2)
    gevent.sleep(2)
    # r=requests.get('http://www.qq.com') # 
    # print(r.status_code)
    print('Implicit context switch back to bar')

start=time.time()
gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar),
])
print('time used {}'.format(time.time()-start))
