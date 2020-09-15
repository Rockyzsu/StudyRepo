#!urs/bin/env python
#coding:utf-8


# 外观模式：为子系统中的一组接口提供一个一致的界面，此模式定义了一个高层接口，这个接口
# 使得这一子系统更加容易使用。[DP]
# 在设计初期阶段，应该要有意识的将不同的两个层分离，比如经典的三层架构，就需要考虑在
# 数据访问层和业务逻辑层，业务逻辑层和表示层的层与层之间建立外观Facade，这样就可以为
# 复杂的子系统提供一个简单的接口，使耦合度大大降低。

'''
UML类图
                                Facade外观类，知道哪些子系统负责处理请求，
----------                      将客户的请求代理给适当的子系统对象。
| Client |——————————————.        /
----------              |       /
                                               ∨            /
                    -----------------           
                    |     Facade    |
--------------------|+MethodA()     |------------SubSystem Classes------------
|                   |+MethodB()     |                                        |
|                   -----------------                                        |
|                           |                                                |
|    .—————————————————————————————————————————————————————.                 |
|    |                   |                |                |                 |
|    ∨                                    ∨                              ∨                              ∨                                 |
| ---------------- ---------------- ------------------ -----------------     |
| | SubSystemOne | | SubSystemTwo | | SubSystemThree | | SubSystemFour |     |
| |+MethodOne()  | |+MethodTwo()  | |+MethodThree()  | |+MethodFour()  |     |
| ---------------- ---------------- ------------------ -----------------     |
|                                                                            |
------------------------------------------------------------------------------
                                \
                    SubSystem Classes子系统类集合
                                       实现子系统的功能，处理Facade对象指派的任务。
                                       注意子类中没有Facade的任何信息，
                                       即没有对Facade对象的引用
'''


class SubSystemOne(object):
    def MethodOne(self):
        print('子系统方法一')
        
class SubSystemTwo(object):
    def MethodTwo(self):
        print('子系统方法二')
        
class SubSystemThree(object):
    def MethodThree(self):
        print('子系统方法三')
        
class SubSystemFour(object):
    def MethodFour(self):
        print('子系统方法四')


class Facade(object):
    # 外观类
    def __init__(self):
        self.one = SubSystemOne()
        self.two = SubSystemTwo()
        self.three = SubSystemThree()
        self.four = SubSystemFour()
        
    def MethodA(self):
        print('方法组A() --- ')
        self.one.MethodOne()
        self.two.MethodTwo()
        self.four.MethodFour()
        
    def MethodB(self):
        print('方法组B() --- ')
        self.two.MethodTwo()
        self.three.MethodThree()


if __name__ == '__main__':
    facade = Facade()
    facade.MethodA()
    facade.MethodB()