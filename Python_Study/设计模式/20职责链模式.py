#!urs/bin/env python
#coding:utf-8



# 职责链模式：使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。
# 将这个对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。[DP]

'''
UML类图

                                                                    定义一个处理请示的接口
                                            /
----------                 ----------------------------------------
| Client |————————————————>|               Handler                |
----------                 |+SetSuccessor(in successor: Handler)  |<——————————————————.
                           |+HandleRequest(in request: int)       |                   |
                           ----------------------------------------                   | 
                                                                                           △                                                                             |
                                              |                                       |
                         .——————————————————————————————————————.                     |
                         |                                      |                     |
            ---------------------------------- ----------------------------------     |
            |    ConcreteHandler1            | |    ConcreteHandler2            |     |
            |+HandleRequest(in request: int) | |+HandleRequest(in request: int) |◇———
            ---------------------------------- ----------------------------------
                                    \                /
                                                                具体处理者类，处理它所负责的请求，
                                                                可访问它的后继者，如果可处理该请求，
                                                                就处理之，否则就将该请求转发给它的后继者
'''


from abc import ABCMeta, abstractmethod


class Handler(metaclass=ABCMeta):
    def __init__(self):
        self.successor = None
        
    def SetSuccessor(self, successor):
        # 设置继任者
        self.successor = successor
        
    @abstractmethod
    def HandleRequest(self, request): return    # 处理请求的抽象方法
    
    
class ConcreteHandler1(Handler):
    def HandleRequest(self, request):
        if (request >=0 and request < 10):
            # 0到10，处理此请求
            print('{0} 处理请求 {1}'.format(self.__class__.__name__, request))
        elif (self.successor):
            # 转移到下一位
            self.successor.HandleRequest(request)


class ConcreteHandler2(Handler):
    def HandleRequest(self, request):
        if (request >= 10 and request < 20):
            print('{0} 处理请求 {1}'.format(self.__class__.__name__, request))
        elif (self.successor):
            self.successor.HandleRequest(request)
            
            
class ConcreteHandler3(Handler):
    def HandleRequest(self, request):
        if (request >= 20 and request < 30):
            print('{0} 处理请求 {1}'.format(self.__class__.__name__, request))
        elif (self.successor):
            self.successor.HandleRequest(request)


def run():
    h1 = ConcreteHandler1()
    h2 = ConcreteHandler2()
    h3 = ConcreteHandler3()
    h1.SetSuccessor(h2)
    h2.SetSuccessor(h3)
    
    requests = [2, 5, 14, 22, 18, 3, 27, 20]
    for i in requests:
        h1.HandleRequest(i)
        

# 由于python自身的特点，可以使用yield进行串联职责链
def start(end):
    num = 0
    while True:
        yield num
        if end == num: break
        num += 1
            

class Base(metaclass=ABCMeta):
    def __init__(self, stream):
        self.stream = stream
        
    @abstractmethod
    def next(self): return

class AddOne(Base):
    def next(self):
        while True:
            num = next(self.stream)
            yield num + 1
            
class AddTwo(Base):
    def next(self):
        while True:
            num = next(self.stream)
            yield num + 2


def run2():
    stream = start(10)
    stream = AddOne(stream).next()
    stream = AddTwo(stream).next()
    for i in stream:
        print(i)

if __name__ == '__main__':
#     run()
    run2()
    