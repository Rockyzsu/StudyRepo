#!urs/bin/env python
#coding:utf-8


# Event：一个阻塞协程的事件直到它的内部标识设置为True。类似于threading.Event，协程
# 可以等待一个事件被设置，一旦它被设置，调用yield event.wait()将不会被阻塞除非该事件
# 已经被清除。


from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Event
event = Event()


@gen.coroutine
def waiter():
    print('Waiting for event')
    yield event.wait()
    print('Not waiting this time')
    yield event.wait()
    print('Done')
    
@gen.coroutine
def setter():
    print('About to set the event')
    event.set()
    
@gen.coroutine
def runner():
    yield [waiter(), setter()]


if __name__ == '__main__':
    IOLoop.current().run_sync(runner)