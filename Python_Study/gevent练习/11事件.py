#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

import gevent

def synchronous():
    # 同步事件驱动
    from gevent.event import Event
    evt = Event()
    def setter():
        print('A: Hey wait for me, I have to do something')
        gevent.sleep(3)
        print('Ok, I\'m done')
        evt.set()
        
    def waiter():
        print('I\'ll wait for you')
        evt.wait()
        print('It\'s about time')
        
    gevent.joinall([gevent.spawn(setter), 
                    gevent.spawn(waiter),
                    gevent.spawn(waiter),
                    gevent.spawn(waiter),
                    gevent.spawn(waiter)
                    ])

def asynchronous():
    # 异步事件驱动
    from gevent.event import AsyncResult
    # 事件对象的一个扩展是AsyncRresult，它允许在唤醒调用上附加一个值。它有时也被
    # 称作是future或defered，因为它持有一个指向将来任意时间可设置为任何值的引用。
    a = AsyncResult()
    
    def setter():
        """
        After 3 seconds set the result of a.
        """
        gevent.sleep(1)
        a.set('Hello!')
        
    def waiter():
        """
        After 3 seconds the get call will unblock after the setter
        puts a value into the AsyncResult.
        """
        print(a.get())
        
    gevent.joinall([
                    gevent.spawn(setter),
                    gevent.spawn(waiter),
                    gevent.spawn(waiter)
                    ])

if __name__ == '__main__':
#     synchronous()
    asynchronous()