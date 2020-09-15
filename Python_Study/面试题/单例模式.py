#!usr/bin/env python
#coding:utf-8

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class MyClass: pass


@singleton
class YouClass: pass

a = MyClass()
b = MyClass()
print(id(a))
print(id(b))

c = YouClass()
d = YouClass()
print(id(c))
print(id(d))