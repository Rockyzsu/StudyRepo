# -*- coding: utf-8 -*-
# @Time    : 2017/7/25 10:59
# @Author  : 卧槽
# @Site    : 
# @File    : 装饰器.py
# @Software: PyCharm


def outer2(func2):
    def inner2(*args, **kwargs):
        print("开始")
        r = func2(*args, **kwargs)
        print("结束")
        return r
    return inner2


def outer1(func1):
    def inner1(*args, **kwargs):
        print('start')
        r = func1(*args, **kwargs)
        print('stop')
        return r
    return inner1


@outer2
@outer1
def f():
    print('这是 f 函数')
# outer1(outer2(f))
f()