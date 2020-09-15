#!urs/bin/env python
#coding:utf-8

# 设计模式
# 第二章 策略模式 
# 策略模式：它定义了算法家族，分别封装起来，让它们之间可以互相替换，此模式让算法的变化，
# 不会影响到使用算法的客户。

'''
UML类图

    CashContext上下文，用一个                  策略类，定义所有支持的
    Cash*来配置，维护一个                      算法的公共接口
        对CashSuper对象的引用                     /
         /                                     /
-------------------------            ------------------------    
|        CashContext    |            |        CashSuper     |    
|+GetResult(): double   |◇————————>|+acceptCash(): double |
-------------------------            ------------------------
                                               △
                                               |
                    .——————————————————————————————————————————————————.
                    |                        |                         |
        ------------------------ ------------------------ ------------------------ 
        |       CashNormal     | |     CashRebate       | |      CashReturn      |
        |+acceptCash(): double | |+acceptCash(): double | |+acceptCash(): double |
        ------------------------ ------------------------ ------------------------
                             \               |             /
                             具体策略类，封装了具体的算法或行为
'''


from abc import ABCMeta, abstractmethod


class CashSuper(metaclass=ABCMeta):
    # 现金收费抽象类
    def __init__(self):
        raise
    
    @abstractmethod
    def acceptCash(self, money): return
    

class CashNormal(CashSuper):
    # 正常收费子类
    def __init__(self): return
    
    def acceptCash(self, money):
        return money
    

class CashRebate(CashSuper):
    # 打折收费子类
    def __init__(self, ld):
        # 打折收费，初始化时，必须要输入折扣率
        self.moneyRebate = ld
        
    def acceptCash(self, money):
        return money * self.moneyRebate
    

class CashReturn(CashSuper):
    def __init__(self, moneyCondition, moneyReturn):
        # 返利收费，初始化时必须要输入返利条件和返利值，比如满300返100，
        # 则moneyCondition为300，moneyReturn为100。
        self.moneyCondition = moneyCondition
        self.moneyReturn = moneyReturn
        
    def acceptCash(self, money):
        result = money
        if (money >= self.moneyCondition):
            # 若大于返利条件，则需要减去返利值，每达到self.moneyCondition这么多数目
            # 都要减去self.moneyReturn
            result = money - (money // self.moneyCondition) * self.moneyReturn
        return result
    
    
class CashContext(object):
    def __init__(self, csuper):
        # 传入具体的收费策略
        self.cs = csuper
        
    def GetResult(self, money):
        # 根据收费策略的不同，获得计算结果
        return self.cs.acceptCash(money)
    
def run(choice):
    # 客户端调用
    if '正常收费' == choice:
        cc = CashContext(CashNormal())
    elif '满300返100' == choice:
        cc = CashContext(CashReturn(300, 100))
    elif '打8折' == choice:
        cc = CashContext(CashRebate(0.8))
    totalPrice = cc.GetResult(713.5)
    print(totalPrice)
    
    
# 策略与简单工厂结合
class CashContext2(object):
    def __init__(self, choice):
        self.cc = None
        if '正常收费' == choice:
            self.cc = CashNormal()
        elif '满300返100' == choice:
            self.cc = CashReturn(300, 100)
        elif '打8折' == choice:
            self.cc = CashRebate(0.8)
        
    def GetResult(self, money):
        return self.cc.acceptCash(money) 
    

if __name__ == '__main__':
    run('正常收费')
    run('满300返100')
    run('打8折')
    
    csuper = CashContext2('正常收费')
    print(csuper.GetResult(713.5)) 
    csuper = CashContext2('满300返100')
    print(csuper.GetResult(713.5)) 
    csuper = CashContext2('打8折')
    print(csuper.GetResult(713.5)) 
    
#     CashSuper()
    
    
# 策略模式是一种定义一系列算法的方法，从概念上来看，所有这些算法完成的都是相同的工作，
# 只是实现不同，它可以以相同的方式调用所有的算法，减少了各种算法类与使用算法之间的耦合。

