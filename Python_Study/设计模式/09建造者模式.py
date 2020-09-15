#!urs/bin/env python
#coding:utf-8


# 如果需要将一个复杂的构建与它的表示分离，使得同样的构建过程可以创建不同的表示的意图时，
# 我们需要应用一个设计模式，“建造者模式”，又叫生成器模式。建造者模式可以将一个产品的
# 内部表象与产品的生产过程分割开来，从而可以使一个建造过程生成具有不同的内部表象的产品
# 对象。如果我们用了建造者模式，那么用户就只需指定需要建造的类型就可以得到它们，而具体
# 建造的过程和细节就不需要知道了。
# 建造者模式：将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的
# 表示。[DP]


'''
UML类图
                                    Builder是为创建一个Product对象的各个
                                                                        部件指定的抽象接口
                                            /
-------------------------            --------------- 
|         Director      |   -builder |    Builder  |
|+Construct()           |◇————————>|+BuildPart() |
-------------------------            ---------------
        /                                  △
指挥者，是构建一个使用                                              |                        具体产品
Builder接口的对象                                       -------------------------           /
                                    |    ConcreteBuilder    |       -----------
                                    |+BuildPart()           |------>| Product |
                                    |+GetResult()           |       -----------
                                    -------------------------
                                                /
                                                        具体建造者，实现Builder接口，构造和装配各个部件
'''                                  


import abc

class PersonBuilder(metaclass=abc.ABCMeta):
    # 抽象的建造人的类
    @abc.abstractmethod
    def BuildHead(self): return
    
    @abc.abstractmethod
    def BuildBody(self): return
    
    @abc.abstractmethod
    def BuildArmLeft(self): return
    
    @abc.abstractmethod
    def BuildArmRight(self): return
    
    @abc.abstractmethod
    def BuildLegLeft(self): return
    
    @abc.abstractmethod
    def BuildLegRight(self): return
    

class PersonDirector(object):
    # 指挥者
    def __init__(self, pb):
        # PersonBuilder-用户告诉指挥者，我需要什么样的小人
        self.pb = pb
        
    def CreatePerson(self):
        self.pb.BuildHead()
        self.pb.BuildBody()
        self.pb.BuildArmLeft()
        self.pb.BuildArmRight()
        self.pb.BuildLegLeft()
        self.pb.BuildLegRight()
    
    
class PersonThinBuilder(PersonBuilder):
    def BuildHead(self): print('画个头')
    
    def BuildBody(self): print('画个瘦身体')
    
    def BuildArmLeft(self): print('画左臂')
    
    def BuildArmRight(self): print('画右臂')
    
    def BuildLegLeft(self): print('画左腿')

    def BuildLegRight(self): print('画右腿')
    

class PersonFatBuilder(PersonBuilder):
    def BuildHead(self): print('画个头')
    
    def BuildBody(self): print('画个胖身体')
    
    def BuildArmLeft(self): print('画左臂')
    
    def BuildArmRight(self): print('画右臂')
    
    def BuildLegLeft(self): print('画大左腿')

    def BuildLegRight(self): print('画大右腿')
    
    

if __name__ == '__main__':
    print('瘦人：')
    ptb = PersonThinBuilder()
    pdThin = PersonDirector(ptb)
    pdThin.CreatePerson()
    
    print('胖人：')
    ftb = PersonFatBuilder()
    pdFat = PersonDirector(ftb)
    pdFat.CreatePerson()