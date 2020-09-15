#!urs/bin/env python
#coding:utf-8


# 享元模式（Flyweight）：运用共享技术有效地支持大量细粒度的对象。[DP]
# 享元模式可以避免大量非常相似类的开销。在程序设计中，有时需要生成大量细粒度的类实例
# 来表示数据。如果发现这些实例除了几个参数外基本都是相同的，有时就能够受大幅度地减少
# 需要实例化的类的数量。如果能把那些参数移到类实例的外面，在方法调用时将它们传递进来，
# 就可以通过共享大幅度地减少单个实例的数目。

# 如果一个应用程序使用了大量对象，而大量的这些对象造成了很大的存储开销时就应该考虑使用；
# 还有就是对象的大多数状态可以是外部状态，如果删除对象的外部状态，那么可以用相对较少的
# 共享对象取代很多组对象，此时可以考虑使用享元模式。


'''
UML 类图

--------------            ---------------------           -----------------------------------
|     用户        |<----------|        网站                |<--------◇|            网站工厂                           |
|+账号:string |           |+使用(in user: 用户)|           |+得到网站分类(in key: strng): 网站|
--------------            ---------------------           |+得到网站分类总数(): int          |
                                                                       △                                          -----------------------------------
                                    |  
                            ---------------------
                            |        具体网站        |
                            |+使用(in user: 用户)|
                            ---------------------
'''


from abc import ABCMeta, abstractmethod

class User(object):
    # 用户
    def __init__(self, name):
        self.name = name
        
    def GetName(self):
        return self.name
    
    
class WebSite(metaclass=ABCMeta):
    @abstractmethod
    def Use(self, user): return # “使用”方法需要传递“用户”
    
    
class ConcreteWebSite(WebSite):
    # 具体网站类
    def __init__(self, name):
        self.name = name
        
    def Use(self, user):
        print('网址分类： ' + self.name + '用户： ' + user.GetName())
        
        
class WebSiteFactory(object):
    # 网站工厂
    def __init__(self):
        self.flyweights = {}
        
    def GetWebSiteCategory(self, key):
        # 获得网站分类
        if key not in self.flyweights:
            self.flyweights[key] = ConcreteWebSite(key)
        return self.flyweights[key]
            
    def GetWebSiteCount(self):
        return len(self.flyweights)
    
    
def run():
    f = WebSiteFactory()
    fx = f.GetWebSiteCategory('产品展示')
    fx.Use(User('小菜'))
    fy = f.GetWebSiteCategory('产品展示')
    fy.Use(User('大鸟'))
    fz = f.GetWebSiteCategory('产品展示')
    fz.Use(User('娇娇'))
    
    fz = f.GetWebSiteCategory('博客')
    fz.Use(User('郭靖'))
    fz = f.GetWebSiteCategory('博客')
    fz.Use(User('丁春秋'))
    fz = f.GetWebSiteCategory('博客')
    fz.Use(User('步惊云'))
    print('得到网址分类总数为%d' % f.GetWebSiteCount())
        

if __name__ == '__main__':
    run()
    