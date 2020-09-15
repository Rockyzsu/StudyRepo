#!urs/bin/env python
#coding:utf-8

import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future

@coroutine
def asyn_sum(a, b):
    print("begin calculate:sum %d+%d"%(a,b))
    future = Future()

    def callback(a, b):
        print("calculating the sum of %d+%d:"%(a,b))
        future.set_result(a+b)
#         return future

    tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)
    result = yield future
#     result = yield callback(a, b)

    print("after yielded")
    print("the %d+%d=%d"%(a, b, result))

# def main():
#     asyn_sum(2,3)
#     tornado.ioloop.IOLoop.instance().start()
    
@coroutine
def main2():
    yield asyn_sum(2, 3)

if __name__ == "__main__":
    tornado.ioloop.IOLoop.instance().run_sync(main2)
