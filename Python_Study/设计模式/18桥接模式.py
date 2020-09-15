#!urs/bin/env python
#coding:utf-8


# 合成/聚合复用原则（CARP）：尽量使用合成/聚合，尽量不要使用类继承。
# 合成/聚合复用原则的好处是，优先使用对象的合成/聚合将有助于保持每个类被封装，并被集中
# 在单个任务上。这样类和类继承层次会保持较小规模，并且不太可能增长为不可控制的庞然大物。

# 桥接模式：将抽象部分与它的实现部分分离，使它们都可以独立地变化。[DP]
# 这里的抽象与它的实现分离并不是说让抽象类与其派生类分离，因为这没有任何意义。实现指
# 的是抽象类和它的派生类用来实现自己的对象[DPE]。

'''
UML类图

                抽象                                                                        实现
------------------                        -----------------
|   Abstraction  |                        |   Implementor |
|+Operation()    |◇———————————————————>|+OperationImp()|
------------------                        -----------------
               △                                                                                △
        |                                         |       
-------------------------        .—————————————————————————————.
|   RefinedAbstraction  |        |                             |   
|+Operation()           | ------------------------ ------------------------
------------------------- | ConcreteImplementorA | | ConcreteImplementorB |
          /               |+OperationImp()       | |+OperationImp()       |
         /                ------------------------ ------------------------
        被提炼的对象                                                              \      /
                                                                                             具体实现
'''         


from abc import ABCMeta, abstractmethod

class Implementor(metaclass=ABCMeta):
    @abstractmethod
    def Operation(self): return
    

class ConcreteImplementorA(Implementor):
    def Operation(self):
        print('具体实现A的方法执行')
        

class ConcreteImplementorB(Implementor):
    def Operation(self):
        print('具体实现B的方法执行')
        
        
class Abstraction(object):
    def __init__(self):
        self.implementor = None
        
    def SetImplementor(self, implementor):
        self.implementor = implementor
        
    def Operation(self):
        self.implementor.Operation()
        
        
class RefinedAbstraction(Abstraction):
    def Operation(self):
        self.implementor.Operation()
        
        
def run():
    ab = RefinedAbstraction()
    ab.SetImplementor(ConcreteImplementorA())
    ab.Operation()
    
    ab.SetImplementor(ConcreteImplementorB())
    ab.Operation()

# 实现系统可能有多角度分类，每一种分类都有可能变化，那么就把这种多角度分离出来让它们
# 独立变化，减少它们之间的耦合。

if __name__ == '__main__':
    run()
    
    