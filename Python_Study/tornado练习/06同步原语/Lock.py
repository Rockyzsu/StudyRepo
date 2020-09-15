#!urs/bin/env python
#coding:utf-8


# Lock：一个Lock开始解锁，然后它立即acquire锁。虽然它是锁着的，一个协程yield acquire
# 并等待，直到另一个协程release。
# 释放一个没锁住的锁将抛出RuntimeError。


from tornado import gen, locks
lock = locks.Lock()

@gen.coroutine
def f():
    with (yield lock.acquire()):
        # Do something holding the lock
        pass
    # Now the lock is released


