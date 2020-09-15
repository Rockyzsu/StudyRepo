#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

# 组是一个运行中greetlet的集合，集合中的greetlet像一个组一样被共同管理和调度。
# 它也兼饰了像multiporicessing库那样的平行调度器的角色。

import gevent
from gevent.pool import Group
def talk(msg):
    n = 3
    while 0 < n:
        print(msg)
        n -= 1
g1 = gevent.spawn(talk, 'bar')
g2 = gevent.spawn(talk, 'foo')
g3 = gevent.spawn(talk, 'fizz')
group = Group()
group.add(g1)
group.add(g2)
group.join()
group.add(g3)
group.join()
