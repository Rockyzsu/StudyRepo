#!urs/bin/env python
#coding:utf-8

# tornado的这些同步原语不是线程安全的，不能用来代替标准中的同步原语。它们是为了协调
# 在单线程中的tornado协程，而不是为了在一个多线程app中保护共享对象。


# Condition：允许一个或多个协程等待直到被通知的条件。就像threading.Condition，但是
# 不需要一个被获取和释放的底层锁。

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Condition
condition = Condition()


@gen.coroutine
def waiter():
    print("I'll wait right here")
    yield condition.wait()  # yield a Future
    print("I'm done waiting")
    
@gen.coroutine
def notifier():
    print('About to notify')
    condition.notify()
    print('Done notifying')
    
@gen.coroutine
def runner():
    # yield two Futures; wait for waiter() and notifier() to finish()
    yield [waiter(), notifier()]


if __name__ == '__main__':
    IOLoop.current().run_sync(runner)
    
    