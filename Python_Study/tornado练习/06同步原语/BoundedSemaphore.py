#!urs/bin/env python
#coding:utf-8


# BoundedSemphore：一个防止release()被调用太多次的信号量。
# 如果release增加信号量的值超过初始值，它将抛出ValueError。信号量通常是通过限制容量
# 来保护资源，所以一个信号量释放太多次是一个错误的标志。


import tornado.locks.BoundedSemaphore
