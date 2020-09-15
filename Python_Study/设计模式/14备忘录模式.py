#!urs/bin/env python
#coding:utf-8


# 备忘录：在不破坏封装性的前提下，捕获一个对象内部状态，并在该对象之外保存这个状态。
# 这样以后就可将该对象恢复到原先保存的状态。[DP]

'''
UML类图

                                                负责存储Originator对象的内部状态，
                                                并可防止Originator以外的其他对象
                                                访问备忘录Memento。
                                        /
                                       /
-------------------------      -----------------         -------------------
|    Originator         |      |    Memento    |         |    Caretaker    |
|+state                 |      |+state         |<——————◇|-Memento: Memento|
|+SetMemento(m: Memento)|----->|               |         |                 |
|+CreateMemento()         |      -----------------         -------------------
-------------------------                                              /
        \                                                             /
         \                                                负责保存好备忘录Memento           
    负责创建一个备忘录Memento，用以记录当前时刻
    它的内部状态，并可使用备忘录恢复内部状态。
'''

class Originator(object):
    # 发起人类
    def __init__(self):
        # 需要保存的属性，可能有多个
        self.state = None
        
    def set(self, v):
        self.state = v
    
    def get(self):
        return self.state
    
    def CreateMemento(self):
        # 创建备忘录，将当前需要保存的信息导入并实例化一个Memento对象
        return Memento(self.state)
    
    def SetMemento(self, memento):
        # 恢复备忘录，将Memento导入并将相关数据恢复
        self.state = memento.get()
        
    def Show(self):
        print('State=' + self.state)
    
    
class Memento(object):
    def __init__(self, state):
        # 构造方法，将相关数据导入
        self.state = state
        
    def get(self):
        # 需要保存的数据属性，可以是多个
        return self.state
    
    
class Caretaker(object):
    # 管理者类
    def __init__(self):
        self.memento = None
        
    def set(self, v):
        # 设置备忘录
        self.memento = v
        
    def get(self):
        # 得到备忘录
        return self.memento
    
    
def run():
    o = Originator()
    o.set('On')
    o.Show()
    
    c = Caretaker()
    # 保存状态时，由于有了很好的封装，可以隐藏Originator的实现细节
    c.set(o.CreateMemento())
    
    o.set('Off')
    o.Show()
    
    o.SetMemento(c.get())
    o.Show()


# Memento模式比较适用于功能比较复杂的，但需要维护或记录属性历史的类，或者需要保存的
# 属性只是众多属性的一小部分时，Originator可以根据保存的Memento信息还原到前一状态。
# 备忘录也是有缺点的，如果对象需要完整存储到备忘录对象中，如果属性状态很大很多，那么
# 在资源消耗上，备忘录对象会非常消耗内存。

if __name__ == '__main__':
    run()
    