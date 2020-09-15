#!urs/bin/env python
#coding:utf-8


# Semaphore：一个信号量管理着代表release调用次数减去acquire的调用次数的计数器加一个
# 初始值。如果必要的话，acquire方法将会阻塞，直到它可以返回，而不使该计数器成为负值。
# 信号量限制访问共享资源，为了允许两个worker同时获得权限，代码如下。


from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Semaphore
sem = Semaphore(2)


@gen.coroutine
def worker(worker_id):
    with (yield sem.acquire()): # acquire()是一个上下文管理器
        print("Worker %d is working" % worker_id)
    print("Worker %d is done" % worker_id)
    sem.release()
    
#     yield sem.acquire()
#     try:
#         print('Worker %d is working' % worker_id)
# #         yield use_some_resource()
#     finally:
#         print('Worker %d is done' % worker_id)
#         sem.release()
        
@gen.coroutine
def runner():
    # Join all workers
    yield [worker(i) for i in range(3)]


if __name__ == '__main__':
    IOLoop.current().run_sync(runner)