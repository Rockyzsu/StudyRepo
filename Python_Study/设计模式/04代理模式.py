#!urs/bin/env python
#coding:utf-8


# 代理模式：为其他对象提供一种代理以控制对整个对象的访问。


class SchoolGirl(object):
    def __init__(self, name):
        self.Name = name
        

class GiveGift(object):
    def GiveDolls(self): return
    def GiveFlowers(self): return
    def GiveChocolate(self): return
    

class Pursuit(GiveGift):
    # 真实执行者
    def __init__(self, mm):
        self.mm = mm
        
    def GiveDolls(self):
        print(self.mm.Name + " 送你洋娃娃")
        
    def GiveFlowers(self):
        print(self.mm.Name + " 送你鲜花")
        
    def GiveChocolate(self):
        print(self.mm.Name + " 送你巧克力")
        

class Proxy(GiveGift):
    # 让代理也去实现送礼物接口
    def __init__(self, mm):
        self.gg = Pursuit(mm)
        
    def GiveDolls(self):
        self.gg.GiveDolls()
        
    def GiveFlowers(self):
        self.gg.GiveFlowers()
        
    def GiveChocolate(self):
        self.gg.GiveChocolate()
        

def run():
    jiaojiao = SchoolGirl('李娇娇')
    proxy = Proxy(jiaojiao)
    
    proxy.GiveDolls()
    proxy.GiveFlowers()
    proxy.GiveChocolate()
        
        
        
if __name__ == '__main__':
    run()