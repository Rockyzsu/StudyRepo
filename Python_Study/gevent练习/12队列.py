#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

import gevent
from gevent.queue import Queue

# put和get都有非阻塞的版本，put_nowait和get_nowait不会阻塞，然而在操作不能完成时抛出
# gevent.queue.Empty或gevent.queue.Empty异常。

tasks = Queue()
def worker(name):
    while not tasks.empty():
        task = tasks.get()
        print('Worker %s got task %s' % (name, task))
        gevent.sleep(0) # 取一个就交出控制权
    print('Quitting time!')
def boss():
    for i in range(1, 5):
        tasks.put_nowait(i)
        
gevent.spawn(boss).join()
gevent.joinall([
gevent.spawn(worker, 'steve'),
gevent.spawn(worker, 'john'),
gevent.spawn(worker, 'nancy'),
])
