#coding:utf-8


# 设计模式
# 第三章 装饰模式 
# 动态地给一个对象添加一些额外的职责，就增加功能来说，装饰模式比生成子类更为灵活。

'''
UML类图

            Component是定义一个对象接口，
                        可以给这些对象动态地添加职责
                        /
                ----------------
                | Component    |<————————————.
                |+Operation()  |             |
                ----------------             |
                                               △                                       |
                        |                    |-component
        .——————————————————————————.         |
        |                          |         |
---------------------        --------------- |          Decorator，装饰抽象类，
| ConcreteComponent |        | Decorator   | |          继承了Component，从外类
|+Operation()       |        |+Operation() |◇                     来扩展Component类的功能，
---------------------        ---------------            但对于Component来说，是
                                                                       △                                     无需知道Decorator的存在的
                                    |
                        .—————————————————————————.
                        |                         |
                ---------------------- ---------------------- 
                | ConcreteDecoratorA | | ConcreteDecoratorB |
                |-addedState: string | |-AddedBehavior()    |
                |+Operation()        | |+Operation()        |
                ---------------------- ----------------------
                            \                /
                        ConcreteDecorator就是具体的装饰对象，
                                                起到给Component添加职责的功能

ConcreteComponent：定义了一个具体的对象，也可以给这个对象添加一些职责
'''                             


import abc

class Component(metaclass=abc.ABCMeta):
    def __init__(self): raise
    
    @abc.abstractmethod
    def Operation(self): return
    

class ConcreteComponent(Component):
    def __init__(self): return
    
    def Operation(self):
        print('具体对象的操作')
        

class Decorator(Component):
    def __init__(self):
        self.component = None
    
    def SetComponent(self, component):  # 设置Component
        self.component = component
        
    def Operation(self):
        # 重写Operation()，实际执行的是Component的Operation()
        if self.component:
            self.component.Operation()
            

class ConcreteDecoratorA(Decorator):
    def __init__(self):
        # 本类特有功能，以区别于ConcreteDecoratorB
        self.addedState = ''
    
    def Operation(self):
        # 首先运行原Component的Operation()，再执行本类的功能，如addedState，相当于
        # 对原Component进行了装饰
        super(ConcreteDecoratorA, self).Operation()
        self.addedState = 'New State'
        print('具体装饰对象A的操作')
        

class ConcreteDecoratorB(Decorator):
    def __init__(self): return
    
    def Operation(self):
        # 首先运行原Component的Operation()，再执行本类的功能，如AddedBehavior()，
        # 相当于对原Component进行了装饰
        super(ConcreteDecoratorB, self).Operation()
        self.AddedBehavior()
        print('具体装饰对象B的操作')
    
    # 本类独有方法，以区别于ConcreteDecoratorA
    def AddedBehavior(self): return
    
    
def run():
    c = ConcreteComponent()
    d1 = ConcreteDecoratorA()
    d2 = ConcreteDecoratorB()
    
    # 装饰的方法是：首先用ConcreteComponent实例化对象c，然后用ConcreteDecoratorA的
    # 实例化对象d1来包装c，再用ConcreteDecoratorB的对象d2包装d1，最终执行d2的Operation()
    d1.SetComponent(c)
    d2.SetComponent(d1)
    d2.Operation()
    
# 如果只有一个ConcreteDecorator类而没有抽象的Component类，那么Decorator类可以是
# ConcreteDecorator的一个子类。同样道理，如果只有一个ConcreteDecorator类，那么就没有
# 必要建立一个单独的Decorator类，而可以把Decorator和ConcreteDecorator的责任合并成一个类。

#===============================================================================
class Person(object):
    def __init__(self, name):
        self.name = name
        
    def show(self):
        print('装扮的：%s' % self.name)
        

class Finery(Person):
    def decorate(self, person):
        self.person = person
        
    def show(self):
        if self.person:
            self.person.show()
            
class TShirts(Finery):
    def show(self):
        print(self.name)
        self.person.show()
        

class BigTrouser(Finery):
    def show(self):
        print(self.name)
        self.person.show()
        
class S(Finery):
    def show(self):
        print(self.name)
        self.person.show()


def main():
    person = Person('大虾')
    a = TShirts('T恤')
    b = BigTrouser('裤子')
    c = S('鞋子')
    a.decorate(person)
    b.decorate(a)
    c.decorate(b)
    c.show()
    
    
if __name__ == '__main__':
#     run()
    main()