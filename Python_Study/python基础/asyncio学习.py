#!urs/bin/env python
#coding:utf-8

import threading
import datetime
import asyncio
import requests

@asyncio.coroutine
def hello():
    print('Hello World! ', threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello Again! ', threading.currentThread())
    
def foo():
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()
    
def foo2():
    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    

@asyncio.coroutine
def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        yield from asyncio.sleep(1)
        
def foo3():
    loop = asyncio.get_event_loop()
    # Blocking call which returns when the display_date() coroutine is done
    loop.run_until_complete(display_date(loop))
    loop.close()
    
@asyncio.coroutine
def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    yield from asyncio.sleep(1.0)
    return x + y

@asyncio.coroutine
def print_sum(x, y):
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))
    
def foo4():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_sum(1, 2))
    loop.close()
    
# Future
@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(1)
    future.set_result('Future is done!')

def foo5():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation(future))
    loop.run_until_complete(future)
    print(future.result())
    loop.close()
    
@asyncio.coroutine
def slow_operation2(future):
    yield from asyncio.sleep(1)
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
def got_result(future):
    print(future.result())
    loop.stop()

def foo6():
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation2(future))
    future.add_done_callback(got_result)
    try:
        loop.run_forever()
    finally:
        loop.close()
  
@asyncio.coroutine      
def foo7():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.baidu.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.bing.com')
    response1 = yield from future1
    response2 = yield from future2
    print(response1.text)
    print(response2.text)


if __name__ == '__main__':
#     foo()
    foo2()
#     foo3()
#     foo4()
#     foo5()
#     foo6()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(foo7())
    loop.close()