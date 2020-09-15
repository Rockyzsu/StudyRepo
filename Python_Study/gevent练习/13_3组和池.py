#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

from gevent.pool import Pool
pool = Pool(2)

def hello_from(n):
    print('Size of pool %s' % len(pool))
pool.map(hello_from, range(3))
