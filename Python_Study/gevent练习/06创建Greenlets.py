#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''
# 创建Greenlets

import gevent
from gevent import Greenlet

def foo(message, n):
    """
    Each thread will be passed the message, and n arguments
    in its initialization.
    """
    gevent.sleep(n)
    print(message)
 
# Initialize a new Greenlet instance running the named function
thread1 = Greenlet.spawn(foo, "Hello", 1)

# Wrapper for creating and runing a new Greenlet from the named 
thread2 = gevent.spawn(foo, "I live!", 2)

# Lambda expressions
thread3 = gevent.spawn(lambda x: x + 1, 2)

threads = [thread1, thread2, thread3]

# Block until all threads complete.
gevent.joinall(threads)
