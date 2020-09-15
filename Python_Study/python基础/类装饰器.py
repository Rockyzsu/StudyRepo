#!urs/bin/env python
#coding:utf-8



def decorator(func):
    def inner(obj, a):
        result = func(obj, a)
        return 10 + result
    return inner


class A(object):
    @decorator
    def done(self, a):
        b = 10 + a
        return b



if __name__ == '__main__':
    a = A()
    print(a.done(20))