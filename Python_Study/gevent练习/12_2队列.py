#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

import gevent
from gevent.queue import Queue, Empty # Empty是异常

tasks = Queue(maxsize=3)
def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1) # decrements queue size by 1
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0) # yielding到另外个Greenlet，合理分配任务
    except Empty:
        print('Quitting time!')
        
def boss():
    """
    Boss will wait to hand out work until a individual workeworker 
    free since the maxsize of the task queue is 3.
    """
    for i in range(1,10):
        tasks.put(i)
    print('Assigned all work in iteration 1')
    for i in range(10,20):
        tasks.put(i)
    print('Assigned all work in iteration 2')
    
gevent.joinall([
                gevent.spawn(boss),
                gevent.spawn(worker, 'steve'),
                gevent.spawn(worker, 'john'),
                gevent.spawn(worker, 'bob'),
])

