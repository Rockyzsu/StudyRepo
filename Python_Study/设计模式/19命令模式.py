#!urs/bin/env python
#coding:utf-8


# 命令模式：将一个请求封装为一个对象，从而使你可用不同的请求对客户进行参数化；对请求
# 排队或记录请求日志，以及支持可撤销的操作。[DP]

# 优点：
# 1. 它能较容易地设计一个命令队列。
# 2. 在需要的情况下，可以较容易地将命令记入日志。
# 3. 允许接收请求的一方决定是否要否决请求。
# 4. 可以容易地实现对请求的撤销和重做。
# 5. 由于加进新的命令类不影响其他的类，因此增加新的具体命令类很容易。

# 敏捷开发原则告诉我们，不要为代码添加基于猜测的、实际不需要的功能。如果不清楚一个系统
# 是否需要命令模式，一般就不要着急去实现它，事实上，在需要的时候通过重构实现这个模式
# 并不困难，只有在真正需要如撤销/恢复操作等功能时，把原来的代码重构为命令模式才有意义。


'''
UML类图                                                                                            
                                                                                        用来声明执行操作的接口
                                要求该命令执行这个请求                                    /
                           \                    ----------------
----------            -----------              |   Command    |
| Client |----------->| Invoker |◇——————————>|+Excute()     |
----------            ------------             ----------------
     |                                               △
     |                                               |
     |                -----------  -receiver   ---------------------
     .--------------->| Receiver |<————————————| ConcreteCommand   |
                      |+Action() |             |-receiver: Receiver|
                      ------------             |+Execute()         |
                           /                   ---------------------
            知道如何实施与执行一个请求相关的                                            /
            操作，任何类都可能作为一个接收者                                          /
                                                                                            将一个接收者对象绑定于一个动作，
                                                                                            调用接收者相应的操作，以实现Execute
'''


from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    # 用来声明执行操作的接口
    def __init__(self, receiver):
        self.receiver = receiver
        
    @abstractmethod
    def Execute(self): return
    
    
class ConcreteCommand(Command):
    # 将一个接收者对象绑定于一个动作，调用接收者相应的操作，以实现Execute。
    def Execute(self):
        self.receiver.Action()
        
      
class Invoker(object):
    # 要求该命令执行这个请求
    def __init__(self):
        self.command = None
        
    def SetCommand(self, command):
        self.command = command
        
    def ExecuteCommand(self):
        self.command.Execute()
        
        
class Receiver(object):
    # 知道如何实施与执行一个与请求相关的操作，任何类都可能作为一个接收者。
    def Action(self):
        print('执行请求！')
        
        
    
if __name__ == '__main__':
    r = Receiver()
    c = ConcreteCommand(r)
    i = Invoker()
    i.SetCommand(c)
    i.ExecuteCommand()
    
    