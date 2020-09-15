#encoding=utf-8

from abc import ABCMeta, abstractmethod

# 观察者模式定义了一种一对多的依赖关系，让多个观察者对象同时监听某一个主题对象。这个
# 主题对象再发生变化时，会通知所有观察者对象，使它们能够自动更新自己。[DP]

# 将一个系统分割成一系列相互协作的类有一个很不好的副作用，那就是需要维护相关对象间的
# 一致性。我们不希望为了维持一致性而使各个类之间紧密耦合，这样维护、扩展和重用都带来不便。
# 使用观察者模式的情形：当一个对象的改变需要同时改变其他对象的时候，而且它不知道具体
# 有多少对象待改变时，应该考虑使用观察者模式。
# 总的来将观察者模式所做的工作其实就是在解除耦合，让耦合的双方都依赖于抽象，而不是依赖
# 于具体。从而使各自的变化都不会影响另一边的变化。


'''
UML类图

        ------------------------------
        |    Subject抽象通知者                |                          --------------
        |+增加(in 观察者: 抽象观察者)  |------------------------->|  抽象观察者 |
        |+减少(in 观察者: 抽象观察者)  |                          |+更新()     |
        |+通知()                      |<---------------          --------------
        |+通知者状态(): string        |                |                 △
        ------------------------------                |                  |
                             △                          △                                              |                  .———————————————.
               |              |                       .----------.       |               |
               |              ——————————————————                 |   ------------- -------------
------------------------------    --------------|--------------- |   |看股票观察者| |看股票观察者 |
|            老板                         |    |            前台                         | |   |+更新()    | |+更新()     |
|+增加(in 观察者: 抽象观察者)  |    |+增加(in 观察者: 抽象观察者) | |   ------------- -------------
|+减少(in 观察者: 抽象观察者)  |    |+减少(in 观察者: 抽象观察者) | |          |             |
|+通知()                      |    |+通知()                     | .-------------------------
|+通知者状态(): string        |    |+通知者状态(): string        |
------------------------------    ------------------------------
'''

class Subject(metaclass=ABCMeta):
    # 通知者接口
    @abstractmethod
    def Attach(self): raise
    
    @abstractmethod
    def Detach(self): raise
    
    @abstractmethod
    def Notify(self): raise
    
    @abstractmethod
    def SetAction(self, value): raise
    
    @abstractmethod 
    def GetAction(self): raise
    
    
class Boss(Subject):
    # 具体的通知者类可能是前台，也可能是老板，它们也许有各自的一些方法，但对于通知者
    # 来说，它们是一样的，所以它们都去实现这个接口
    def __init__(self):
        self.observers = []
        self.action = None
        
    def Attach(self, observer):
        # 增加
        self.observers.append(observer)
        
    def Detach(self, observer):
        # 减少
        self.observers.remove(observer)
        
    def Notify(self):
        # 通知
        for observer in self.observers:
            observer.Update()
            
    # 老板状态
    def SetAction(self, value):
        self.action = value
        
    def GetAction(self):
        return self.action
   
# 前台秘书类与老板类类似，略。

class Observer(metaclass=ABCMeta):
    # 抽象观察者
    def __init__(self, name, sub):
        self.name = name
        self.sub = sub  # 通知者
        
    @abstractmethod
    def Update(self): return
    
    
class StockObserver(Observer):
    def Update(self):
        print('{0} {1}关闭股票行情，继续工作！'.format(self.sub.action, self.name))
    
        
class NBAObserver(Observer):
    def Update(self):
        print('{0} {1}停止看NBA，继续工作！'.format(self.sub.action, self.name))


def run():
    # 普通观察者
    huhansan = Boss()   # 老板胡汉三
    tongshi1 = StockObserver('老魏', huhansan)
    tongshi2 = NBAObserver('李磊', huhansan)
    huhansan.Attach(tongshi1)
    huhansan.Attach(tongshi2)
#     huhansan.Detach(tongshi1)
    
    # 老板回来
    huhansan.SetAction('我胡汉三回来了！')
    # 发出通知
    huhansan.Notify()
    
    
#==============================================================================#    
# 观察者模式的不足：抽象通知者还是依赖抽象观察者，也就是说，万一没有了抽象观察者这样
# 的接口，通知功能就完不成了。另外就是每个具体观察者，它不一定是“更新”的方法要调用。
# 如果通知者和观察者之间根本就互相不知道，让客户端来决定通知谁，那就很好了。


# 事件委托实现
# “看股票观察者”类和“看NBA观察者”类，去掉了父类“抽象观察类”，所以补上一些代码，并将
# “更新”方法改为各自适合的方法名。
class Observer2(object):
    def __init__(self, name, sub):
        self.name = name
        self.sub = sub  # 通知者
        
        
class StockObserver2(Observer2):
    def CloseStockMarket(self):
        print('{0} {1}关闭股票行情，继续工作！'.format(self.sub.action, self.name))
    
        
class NBAObserver2(Observer2):
    def CloseNBADirectSeeding(self):
        print('{0} {1}停止看NBA，继续工作！'.format(self.sub.action, self.name))

# 抽象通知者由于不希望依赖抽象观察者，所以“增加”和“减少”的方法也就没有必要了（抽象观察
# 者已经不存在了）。
class Subject2(metaclass=ABCMeta):
    # 通知者接口
    @abstractmethod
    def SetAction(self, value): raise
    
    @abstractmethod 
    def GetAction(self): raise
    
    
class Boss2(Subject2):
    def __init__(self):
        self.Update = delegate()
        self.action = None
        
    def Notify(self):
        # 在访问“通知”方法时，调用更新
        self.Update()
            
    # 老板状态
    def SetAction(self, value):
        self.action = value
        
    def GetAction(self):
        return self.action
    
    
class delegate(object):
    # 事件委托
    # 委托是一种引用方法类型。一旦为委托分配了方法，委托将与该方法具有完全相同的行为。
    # 委托方法的使用可以像其他任何方法一样，具有参数和返回值。委托可以看作是函数的
    # 抽象，是函数的“类”，委托的实例将代表一个具体的函数。
    # 一个委托可以搭载多个方法，所有方法被依次唤起。更重要的是，它使得委托对象所搭载
    # 的方法并不需要属于同一个类。
    # 但是委托也是有前提的，那就是委托对象所搭载的所有方法必须具有相同的原型和形式，
    # 也就是拥有相同的参数列表和返回值类型。
    def __init__(self, *calls, **opts):
        for call in calls:
            if not callable(call):
                raise RuntimeError(str(call) + ' not a callable object')
        self.calls = () + calls
        
    def __call__(self, *args, **kwargs):
        try:
            result = None
            for call in self.calls:
                result = call(*args, **kwargs)
            return result
        except TypeError:
            raise RuntimeError('Invalid callable type: ' + str(call))

    def __iadd__(self, *calls):
        # 元组加上一个元组是可以的
        self.calls += calls
        return self


def run2():
    # 事件委托
    huhansan = Boss2()   # 老板胡汉三
    tongshi1 = StockObserver2('老魏', huhansan)
    tongshi2 = NBAObserver2('李磊', huhansan)
    # 将“看股票者”的“关闭股票程序”方法和“看NBA者”的“关闭NBA直播”方法挂钩到“老板”的
    # “更新”上，也就是将两个不同类的不同方法委托给“老板”类的“更新”了。
    huhansan.Update += delegate(tongshi1.CloseStockMarket)
    huhansan.Update += delegate(tongshi2.CloseNBADirectSeeding)
    # 老板回来
    huhansan.SetAction('我胡汉三回来了！')
    # 发出通知
    huhansan.Notify()        
        
if __name__ == '__main__':
#     run()
    run2()
    
    