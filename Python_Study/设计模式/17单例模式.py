#!urs/bin/env python
#coding:utf-8


# 单例模式：保证一个类只有一个实例，并提供一个访问它的全局访问点。[DP]
# 通常我们可以让一个全局变量使得一个对象被访问，但它不能防止你实例化多个对象。一个最好
# 的办法就是，让类自身负责保存它的唯一实例。这个类可以保证没有其他实例可以被创建，并且
# 它可以提供一个访问该实例的方法。[DP]

'''
UML类图

-----------------------
|    Singleton        |
|-instance: Singleton |-----------Singleton类，定义一个GetInstance操作，允许客户
|-Singleton()         |            访问它的唯一实例。GetInstance是一个静态方法，
|+GetInstance()       |            主要负责创建自己的唯一实例。
-----------------------
python实现和Java、C#等不太一样
'''


class Singleton(object):
    _instance = None
    def __new__(self, *args, **kwargs):
        if not Singleton._instance:
            Singleton._instance = object.__new__(self, *args, **kwargs)
        return Singleton._instance
    

def run():
    a = Singleton()
    print(a)
    b = Singleton()
    print(b)
    print('a is b?', a is b)
        
        
if __name__ == '__main__':
    run()
