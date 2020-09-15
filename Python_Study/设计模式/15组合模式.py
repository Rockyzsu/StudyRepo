#!urs/bin/env python
#coding:utf-8


# 组合模式：将对象组合成属性结构以表示“部分-整体”的层次结构。组合模式使得用户对单个
# 对象和组合对象的使用具有一致性。[DP]

'''
UML类图

                                                    组合中的对象声明接口，在适当情况下，实现
                                                     所有类共有接口的默认行为。声明一个接口用
                                                     于访问和管理Component的子部件
                                        /
                           ---------------------------
----------------           |        Component        |
|    Client    |——————————>|+Add(in c: Component)    |
----------------           |+Remove(in c: Component) |<———————————————.                
                           |+Display(in depth: int)  |                |
                           ---------------------------                |
                                                                               △                                                         |
                                        |                             |
                    .————————————————————————————————————.            |
                    |                                    |            |
            --------------------------    --------------------------- |
            |         Leaf           |    |        Composite        | |
            |+Display(in depth: int) |    |+Add(in c: Component)    |◇
            --------------------------    |+Remove(in c: Component) |
                   /                      |+Display(in depth: int)  |
                  /                       ---------------------------
    在组合中表示叶节点对象，                                                         /
    叶节点没有子节点                                    定义有枝节点行为，用来存储子部件，
                                                                      在Component接口中实现与子部件有关的操作，
                                                                      比如Add和删除Remove
'''


from abc import ABCMeta, abstractmethod


class Component(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
  
    # 通常否用Add和Remove方法来提供增加或移除树叶或树枝的功能      
    @abstractmethod
    def Add(self, c):  return
    
    @abstractmethod
    def Remove(self, c): return
    
    @abstractmethod
    def Display(self, depth): return   
    
    
class Leaf(Component):
    # 由于叶子没有再增加分枝和树叶，所以Add和Remove方法实现它没有意义，但这样做可以
    # 消除叶节点和枝节点对象再抽象层次的区别，它们具备完全一致接口。
    def Add(self, c):
        print('Cannot add to a leaf')
        
    def Remove(self, c):
        print('Cannot remove from a leaf')
        
    def Display(self, depth):
        # 叶节点的具体方法，此处是显示其名称和级别
        print('-' * depth + self.name)
        
        
class Composite(Component):
    def __init__(self, name):
        self.children = []  # 一个子对象集合用来存储其下属的枝节点和叶节点
        super(Composite, self).__init__(name)
        
    def Add(self, c):
        self.children.append(c)
        
    def Remove(self, c):
        self.children.remove(c)
        
    def Display(self, depth):
        # 显示其枝节点名称，并对其下级进行遍历
        print('-' * depth + self.name)
        for component in self.children:
            component.Display(depth + 2)
            
# 树叶的Add和Remove实现为空，这种方式叫做透明方式，也就是说在Component中声明所有用来
# 管理子对象的方法，其中包括Add、Remove等。这样实现Component接口的所有子类都具备了
# Add和Remove。这样做的好处就是叶节点和枝节点对于外界没有区别，它们具备完全一致的行为
# 接口。但问题也很明显，因为Leaf类本身不具备Add()、Remove()方法的功能，所以实现它是
# 没有意义的。
# 安全方式：也就是在Component接口中不去声明Add和Remove方法，那么子类的Leaf也就不需要
# 去实现它，而是在Composite声明所有用来管理子类对象的方法，这样做就不会出现刚才提到的
# 问题，不过由于不够透明，所以树叶和树枝类将不具有相同的接口，客户端的调用需要做相应
# 判断，带来了不便。

# 何时使用组合模式：
# 当需求中是体现部分与整体层次的结构时，以及希望用户可以忽略组合对象与单个对象的不同，
# 统一地使用组合结构中的所有对象时，就应该考虑用组合模式了。
        

def run():
    root = Composite('树干')
    root.Add(Leaf('叶子 A'))
    root.Add(Leaf('叶子 B'))
    comp = Composite('树枝 X')
    comp.Add(Leaf('叶子 XA'))
    comp.Add(Leaf('叶子 XB'))
    root.Add(comp)
    
    comp2 = Composite('树枝 XY')
    comp2.Add(Leaf('叶子 XYA'))
    comp2.Add(Leaf('叶子 XYB'))
    comp.Add(comp2)
    
    root.Add(Leaf('叶子 C'))
    leaf = Leaf('叶子 D')
    root.Add(leaf)
    root.Remove(leaf)
    
    root.Display(0)


if __name__ == '__main__':
    run()
    