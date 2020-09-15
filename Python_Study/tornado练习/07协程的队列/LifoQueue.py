#!urs/bin/env python
#coding:utf-8



# LifoQueue：一个后进先出(Lifo)的 Queue.
from tornado.queues import LifoQueue

q = LifoQueue()
q.put(3)
q.put(2)
q.put(1)

print(q.get_nowait())
print(q.get_nowait())
print(q.get_nowait())
