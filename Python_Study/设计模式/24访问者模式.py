#!urs/bin/env python
#coding:utf-8

# 访问者模式：表示一个作用域某对象结构中的各元素的操作。它使你可以在不改变各元素的类
# 的前提下定义作用于这些元素的新操作。[DP]
# 访问者模式适用于数据结构相对稳定的系统。它把数据结构和作用域结构上的操作之间的耦合
# 解脱开，使得操作集合可以相对自由地演化。
# 访问者模式的目的是要把处理从数据结构分离出来。很多系统可以按照算法和数据结构分开，
# 如果这样的系统有比较稳定的数据结构，又有易于变化的算法的话，使用访问者模式就是比较
# 合适的，因为访问者模式使得算法操作的增加变得容易。
# 访问者模式的优点就是增加新的操作容易，因为增加新的操作就意味着增加一个新的访问者。
# 访问者模式将有关的行为集中到一个访问者对象中。
# 访问者模式的缺点也就是使增加新的数据结构变得困难了。


from abc import ABCMeta, abstractmethod


class Action(metaclass=ABCMeta):
    # 状态的抽象类和人的抽象类
    @abstractmethod
    def GetManConclusion(self, concreteElementA): return
    
    @abstractmethod
    def GetWomanConclusion(self, concreteElementB): return
    
    
class Person(metaclass=ABCMeta):
    @abstractmethod
    def Accept(self, visitor): return
    
    @abstractmethod
    def GetType(self): return
        
    
class Success(Action):
    # 成功
    def GetManConclusion(self, concreteElementA):
        print('{0} {1}时，背后多半有一个伟大的女人。'\
              .format(concreteElementA.GetType(), self.GetType())
              )
        
    def GetWomanConclusion(self, concreteElementB):
        print('{0} {1}时，背后多半有一个不成功的男人。'\
              .format(concreteElementB.GetType(), self.GetType())
              )
        
    def GetType(self): return '成功'
    
    
class Failing(Action):
    # 失败
    def GetManConclusion(self, concreteElementA):
        print('{0} {1}时，闷头喝酒，谁也劝不动。'\
              .format(concreteElementA.GetType(), self.GetType())
              )
        
    def GetWomanConclusion(self, concreteElementB):
        print('{0} {1}时，眼泪汪汪，谁也劝不了。'\
              .format(concreteElementB.GetType(), self.GetType())
              )
        
    def GetType(self): return '失败'


class Amativeness(Action):
    # 恋爱
    def GetManConclusion(self, concreteElementA):
        print('{0} {1}时，凡是不懂也要装懂。'\
              .format(concreteElementA.GetType(), self.GetType())
              )
        
    def GetWomanConclusion(self, concreteElementB):
        print('{0} {1}时，遇事懂也装作不懂。'\
              .format(concreteElementB.GetType(), self.GetType())
              )
        
    def GetType(self): return '恋爱'


class Man(Person):
    # 男人
    def Accept(self, visitor):
        visitor.GetManConclusion(self)
        
    def GetType(self): return '男人'
        
        

class Woman(Person):
    # 女人
    def Accept(self, visitor):
        visitor.GetWomanConclusion(self)
        
    def GetType(self): return '女人'
        
        
class ObjectStructure(object):
    # 对象结构
    def __init__(self):
        self.elements = []
        
    def Attach(self, element):
        # 增加
        self.elements.append(element)
        
    def Detach(self, element):
        # 移除
        self.elements.remove(element)
        
    def Display(self, visitor):
        # 查看显示
        for e in self.elements:
            e.Accept(visitor)

# Added
class Marriage(Action):
    # 结婚
    def GetManConclusion(self, concreteElementA):
        print('{0} {1}时，感慨道：恋爱游戏终结时，“有妻徒刑”遥无期。'\
              .format(concreteElementA.GetType(), self.GetType())
              )
        
    def GetWomanConclusion(self, concreteElementB):
        print('{0} {1}时，欣慰曰：爱情长跑路漫漫，婚姻保险保平安。'\
              .format(concreteElementB.GetType(), self.GetType())
              )
        
    def GetType(self): return '结婚'

if __name__ == '__main__':
    o = ObjectStructure()
    o.Attach(Man())
    o.Attach(Woman())
    
    # 成功时的反应
    v1 = Success()
    o.Display(v1)
    # 失败时的反应
    v2 = Failing()
    o.Display(v2)
    # 恋爱时的反应
    v3 = Amativeness()
    o.Display(v3)
    
    # Add
    v4 = Marriage()
    o.Display(v4)
    