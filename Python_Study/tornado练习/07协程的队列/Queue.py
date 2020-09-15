#!urs/bin/env python
#coding:utf-8

# Queue：协调生产者消费者协程。
# 如果maxsize是0（默认）意味着队列的大小是无限的。

'''
QueueEmpty
exception tornado.queues.QueueEmpty[源代码]
当队列中没有项目时, 由 Queue.get_nowait 抛出.
QueueFull
exception tornado.queues.QueueFull[源代码]
当队列为最大size时, 由 Queue.put_nowait 抛出.

'''


from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
q = Queue(maxsize=2)

@gen.coroutine
def consumer():
    while True:
        item = yield q.get()
        try:
            print('Doing work on %s' % item)
            yield gen.sleep(0.01)
        finally:
            q.task_done()
            
@gen.coroutine
def producer():
    for item in range(5):
        yield q.put(item)
        print('Put %s ' % item)

@gen.coroutine
def main():
    # Start consumer without waiting (since it never finishes).
    IOLoop.current().spawn_callback(consumer)
    yield producer()    # Wait for producer to put all tasks
    yield q.join()      # Wait for consumer to finish all tasks
    print('Done')


if __name__ == '__main__':
    IOLoop.current().run_sync(main)
    