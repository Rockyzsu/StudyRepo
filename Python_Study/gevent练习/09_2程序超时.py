#!urs/bin/env python
#coding:utf-8


import gevent
from gevent import Timeout

seconds = 10

def foo1():
    timeout = Timeout(seconds)
    timeout.start()
    
    def wait():
        gevent.sleep(10)
        
    try:
        gevent.spawn(wait).join()
    except Timeout:
        print('Could not complete')
    else:
        print('Complete!')
        

def foo2():
    # 超时类也可以在上下文管理器中使用
    time_to_wait = 5
    
    class TooLong(Exception):
        pass
    with Timeout(time_to_wait, TooLong):
        gevent.sleep(10)

def foo3():
    # 对各种Greenlet和数据结构相关的调用，gevent也提供了超时参数
    def wait():
        gevent.sleep(2)
        
    timer = Timeout(5).start()  # 5s没跑完就抛出Timeout异常
    thread1 = gevent.spawn(wait)
    
    try:
        thread1.join(timeout=timer)
    except Timeout:
        print('Thread 1 timed out')
    else:
        print('Thread 1 complete')
    
    timer = Timeout.start_new(1)
    thread2 = gevent.spawn(wait)
    
    try:
        thread2.get(timeout=timer)
    except Timeout:
        print('Thread 2 timed out')
        
    try:
        gevent.with_timeout(1, wait)
    except Timeout:
        print('Thread 3 timed out')

if __name__ == '__main__':
#     foo1()
#     foo2()
    foo3()
