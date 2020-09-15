#!usr/bin/env python
#coding:utf-8


# 建议50：利用模块实现单例模式
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not Singleton._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
    
    
# 建议51：用户mixin模式让程序更加灵活
# python3中对象已经没有了__bases__属性。


# 建议52：用发布订阅模式实现松耦合
'''
发布订阅者模式：消息的发送者（发布者）不会发送其消息给特定的接收者（订阅者），而是将
发布的消息分为不同的类别直接发布，并不关注订阅者是谁。而订阅者可以对一个或多个类别感
兴趣，且只接收感兴趣的消息，并且不关注是哪个发布者发布的消息。
中间代理人一般被称为Broker
'''
from collections import defaultdict
route_table = defaultdict(list)
class Broker(object):
    @staticmethod
    def sub(channel, callback):
        if callback in route_table[channel]:
            return
        route_table[channel].append(callback)
        
    @staticmethod
    def pub(channel, *a, **kw):
        for func in route_table[channel]:
            func(*a, **kw)

def func_52():
    def greeting(name):
        print('Hello, %s.' % name)
    Broker.sub('greet', greeting)
    Broker.pub('greet', 'LaiYonghao')
    

# 建议53：用状态模式美化代码：
# 略。

if __name__ == '__main__':
#     a = Singleton()
#     b = Singleton()
#     print(id(a) == id(b))
    func_52()
