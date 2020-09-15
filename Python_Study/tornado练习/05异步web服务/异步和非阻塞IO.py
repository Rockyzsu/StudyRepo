#!urs/bin/env python
#coding:utf-8


# 几种风格的异步接口
# 1. 回调函数
# 2. 返回一个占位符（Future， Promise， Deferred）
# 3. 传送给一个队列
# 4. 回调注册表（POSIX信号）
# 不论使用哪种类型的接口，按照定义，异步函数与它们的调用者都有着不同的交互方式；也没有
# 什么对调用者透明的方式使得同步函数异步（类似gevent使用轻量级线程的系统性能虽然堪比
# 异步系统，但它们并没有真正的让事情异步）。


# 一个简单的同步函数
from tornado.httpclient import HTTPClient
def synchronous_fetch(url):
    http_client = HTTPClient()
    response =http_client.fetch(url)    # 同步的HTTPClient返回的不是future
    return response.body.decode()

# 用回调参数重写为异步函数：
from tornado.httpclient import AsyncHTTPClient
def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        print('OK')
        callback(response.body)
    http_client.fetch(url, callback=handle_response)
    
# 使用Future代替回调
from tornado.concurrent import Future
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(lambda f: my_future.set_result(f.result()))
    return my_future
# future版本是推荐方式，因为它有两个主要的优势。首先是错误处理更加一致，因为Future.result
# 可以简单地抛出异常（相较于常见的回调函数接口特别指定错误处理），而且Future很适合和
# 协程一起使用。

from tornado import gen
@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)
# raise gen.Return(response.body)声明是在python2（and 3.2）下人为执行的，因为在其中
# 生成器不允许返回值。为了克服这个问题，tornado的协程抛出一种特殊的叫Return的异常，协程
# 捕获这个异常并把它作为返回值。在python3.3和更高版本，使用return response.body有
# 相同的效果。


import threading
import time
end = lambda t: time.time() - t
def foo1():
    t = time.time()
    ts = []
    url = 'http://cn.bing.com/search?q=China'
    for _ in range(10):
#         thread = threading.Thread(target=synchronous_fetch, args=(url,))
        thread = threading.Thread(target=async_fetch_future, args=(url,))
#         thread = threading.Thread(target=fetch_coroutine, args=(url,))
        ts.append(thread)
    [i.start() for i in ts]
    [i.join() for i in ts]
    print(end(t))
    
inner = lambda x: x
def foo2():
    t = time.time()
    ts = []
    url = 'http://cn.bing.com/search?q=China'
    for _ in range(10):
        thread = threading.Thread(target=asynchronous_fetch, args=(url, inner))
        ts.append(thread)
    [i.start() for i in ts]
    [i.join() for i in ts]
    print(end(t))
    
from tornado.ioloop import IOLoop
def foo3():
    @gen.coroutine
    def inner():
        body = yield fetch_coroutine('http://cn.bing.com/search?q=China')
        print(body)
    IOLoop.current().run_sync(inner)
    
    
    
if __name__ == '__main__':
#     foo1()
    foo2()
#     foo3()