#!urs/bin/env python
#coding:utf-8


# PriorityQueue：一个又优先级的Queue最小的最最优先。
# 写入条目通常是元组，类似（proority number, data）。


from tornado.queues import PriorityQueue

q = PriorityQueue()
q.put((1, 'medium-priority item'))
q.put((0, 'high-priority item'))
q.put((10, 'low-priority item'))

print(q.get_nowait())
print(q.get_nowait())
print(q.get_nowait())

