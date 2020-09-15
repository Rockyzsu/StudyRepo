#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

import gevent
from gevent import getcurrent   # 获得当前Greenlet
from gevent.pool import Group
group = Group()

def hello_from(n):
    print('Size of group %s' % len(group))
    print('Hello from Greenlet %s' % id(getcurrent()))
group.map(hello_from, range(3))


def intensive(n):
    gevent.sleep(3 - n)
    return 'task', n

print('Ordered')    # 有序

ogroup = Group()
for i in ogroup.imap(intensive, range(3)):
    print(i)
    
print('Unordered')  # 无序

igroup = Group()
for i in igroup.imap_unordered(intensive, range(5)):
    print(i)
