#!urs/bin/env python
#coding:utf-8


# 中介者（Mediator）模式：用一个中介对象来封装一系列的对象交互。中介者使各个对象不需要
# 显式地相互引用，从而使耦合松散，而且可以独立地改变它们之间的交互。[DP]


'''
UML类图
    
抽象中介者，定义了同事
对象到中介者对象的接口                                        抽象同事类
      /                                      /
------------                           -------------
| Mediator |<————————————————————————◇| Colleague |
------------           -mediator       -------------
         △                                                                            △
     |                        .—————————————-|——————————.
     |                        |                         |
-------------------- ---------------------- ---------------------- 具体同事类，每个具体
| ConcreteMediator | | ConcreteColleague1 | | ConcreteColleague2 | 同事只知道自己的行为，
-------------------- ---------------------- ---------------------- 而不了解其他同事类的
    /   |                      ∧                                       ∧                         情况，但它们却都认识
   /    |______________________|                     |             中介者对象。
  /     |____________________________________________|
 / 
具体中介者对象，实现抽象类的方法，
它需要知道所有具体同事类，并从具体
同事接收消息，向具体同事对象发出命令      
        
'''


from abc import ABCMeta, abstractmethod

class Mediator(metaclass=ABCMeta):
    # 抽象中介者
    @abstractmethod
    def Send(self, message, colleague): return
    # 定义一个抽象的发送消息方法，得到同事对象和发送消息
    
    
class Colleague(Mediator):
    # 抽象同事
    def __init__(self, mediator):
        # 得到中介者对象
        self.mediator = mediator
        

class ConcreteMediator(Mediator):
    # 具体中介者
    def __init__(self):
        # 需要了解所有的具体同事对象
        self.colleague1 = None
        self.colleague2 = None
        
    def Send(self, message, colleague):
        # 重写发送信息的方法，根据对象做出选择判断，通知对象
        if (colleague == self.colleague1):
            self.colleague2.Notify(message)
        else:
            self.colleague1.Notify(message)
            
            
class ConcreteColleague1(Colleague):
    # 同事1
    def Send(self, message):
        # 发送信息时通常是中介者发送出去的
        self.mediator.Send(message, self)
        
    def Notify(self, message):
        print('同事1得到信息：', message)
        
        
class ConcreteColleague2(Colleague):
    # 同事2
    def Send(self, message):
        self.mediator.Send(message, self)
        
    def Notify(self, message):
        print('同事2得到信息：', message)
        
        
def run():
    m = ConcreteMediator()
    c1 = ConcreteColleague1(m)  # 让两个具体同事类认识中介者对象
    c2 = ConcreteColleague2(m)
    m.colleague1 = c1           # 让中介者认识各个具体同事类对象
    m.colleague2 = c2
    
    c1.Send('吃过饭了吗？')      # 具体同事类对象的发送信息都是通过中介者转发
    c2.Send('没有呢，你打算请客？')

if __name__ == '__main__':
    run()
    