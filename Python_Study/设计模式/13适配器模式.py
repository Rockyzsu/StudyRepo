#!urs/bin/env python
#coding:utf-8


# 适配器模式：将一个类的接口转换成客户希望的另外一个接口。Adapter模式使得原本由于接口
# 不兼容而不能一起工作的那些类可以一起工作。
# 在系统的数据和行为都正确，但接口不符时，我们应该考虑用适配器，目的是使控制范围之外
# 的一个原有对象与某个接口匹配。适配器模式主要应用于希望复用一些现存的类，但是接口又与
# 复用环境要求不一致的情况。
# 在GoF的设计模式中，对适配器模式讲了两种类型，类适配器模式和对象适配器模式，由于类
# 适配器模式通过多重继承对一个接口与另一个接口进行匹配，而C#、VB.NET、JAVA等语言都不
# 支持多重继承（C++支持）。

# 一般在后期为维护在双方都不太容易修改的时候再使用适配器模式适配，而不是一有不同时就
# 使用它。特殊情况是比如公司设计一系统时考虑使用第三方开发组件，而这个组件的接口与我们
# 自己的系统接口是不相同的，而我们也完全没必要为了迎合它而改动自己的接口。


class Target(object):
    # 客户所期待的接口，目标可以是具体的或抽象的类，也可以是接口。
    def Request(self):
        print('普通请求！')
        

class Adaptee(object):
    # 需要适配的类
    def SpecificRequest(self):
        print('特殊请求！')
        
        
class Adapter(Target):
    # 通过在内部包装一个Adaptee对象，把源接口转换成目标接口）
    def __init__(self):
        self.adaptee = Adaptee()
        
    def Request(self):
        # 这样就可以把表面上调用Request()方法变成实际调用SpecificRequest()
        self.adaptee.SpecificRequest()
        
    
def run1():
    target = Adapter()
    target.Request()
    
    
class Player(object):
    # 球员
    def __init__(self, name):
        self.name = name
        
    def Attack(self): return
    def Defense(self): return
    
    
class Forwards(Player):
    # 前锋
    def Attack(self):
        print('前锋 {0} 进攻'.format(self.name))
        
    def Defense(self):
        print('前锋 {0} 防守'.format(self.name))
        

class Center(Player):
    # 中锋
    def Attack(self):
        print('中锋 {0} 进攻'.format(self.name))
        
    def Defense(self):
        print('中锋 {0} 防守'.format(self.name))
        
        
class Guards(Player):
    # 后卫
    def Attack(self):
        print('后卫 {0} 进攻'.format(self.name))
        
    def Defense(self):
        print('后卫 {0} 防守'.format(self.name))
        

class ForeignCenter(object):
    # 外籍中锋
    def __init__(self, name):
        self.name = name
        
    def Attack_(self):
        print('外籍中锋 {0} 进攻'.format(self.name))
        
    def Defense_(self):
        print('外籍中锋 {0} 防守'.format(self.name))
        
        
class Translator(Player):
    # 翻译者
    def __init__(self, name):
        # 声明并实例化一个内部“外籍中锋”对象，表明翻译者与外籍球员有关联
        self.wjzf = ForeignCenter(name)
        Player.__init__(self, name)
        
    def Attack(self):
        self.wjzf.Attack_()
        
    def Defense(self):
        self.wjzf.Defense_()


def run2():
    b = Forwards('巴蒂尔')
    b.Attack()
    m = Guards('麦迪')
    m.Attack()
    ym = Translator('姚明')
    ym.Attack()
    ym.Defense()


if __name__ == '__main__':
#     run1()
    run2()