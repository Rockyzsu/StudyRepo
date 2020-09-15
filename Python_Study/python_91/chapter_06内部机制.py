#!usr/bin/env python
#coding:utf-8


# 建议54：理解built-in objects
# 新式类的元类为type类


# 建议55：__init__()不是构造方法
'''
1. object.__new__(cls, [, args...])：其中cls代表类，args为参数列表。
2. object__init__(self, [, args...])：其中self代表实例对象，args为参数列表
不同点：
1. __new__()方法一般需要返回类的对象，当返回类的对象时将会自动调用__init__()方法进行
初始化，如果没有对象返回，则__init__()方法不会被调用。__init__()不需要显式返回，默认
为None，否则会在运行时抛出TypeError。
2. 当需要控制实例创建的时候可使用__new__()方法，而控制实例初始化的时候使用__init__()方法。
3. 一般情况下不需要覆盖__new__()方法，但当子类继承自不可变类型，如str、int、或者tuple
的时候，往往需要覆盖该方法。
4. 当需要覆盖__new__()和__init__()方法的时候这两个方法的参数必须保持一致，如果不一致
将导致异常。
覆盖__new__()的情况：
1. 当类继承（str、int、tuple或者frozenset等）不可变类型且默认的__new__()方法不能满足
需求的时候。
2. 用来实现工厂模式或者单例模式或者进行元类编程（元类编程中常常需要使用__new__()来控制
对象创建）的时候。
3. 作为用来初始化__init__()方法在多继承的情况下，子类的__init__()方法如果不显式调用
父类的__init__()方法，则父类的__init__()方法不会被调用。
'''
def func_55():
    class UserSet(frozenset):
        def __new__(cls, *args):
            # 须实现这个构造函数才能成功
            if args and isinstance(args[0], str):
                print('args: ',args)
                args = (args[0].split(), ) + args[1:]
                print('args: ',args)
#             return super(UserSet, cls).__new__(cls, *args)
            return frozenset.__new__(cls, *args)
        
        def __init__(self, arg=None):
            print('arg: ',arg)
            if isinstance(arg, str):
                arg = arg.split()
                print('if arg',arg)
            frozenset.__init__(arg)
#             super(UserSet, self).__init__()
            
    print(UserSet('I am testing '))
    print(frozenset('I am testing '))
    
    
# 建议56：理解名字查找机制
'''
1. 局部作用域
一般来说函数的每次调用都会创建一个新的本地作用域，拥有新的命名空间。因此函数内的变量名
可以与函数外的其他变量相同，由于其命名空间不同，并不会产生冲突。默认情况下函数内部任意
的赋值操作（包括=语句、import语句、def语句、参数传递等）所定义的变量名，如果没有用
global语句，则声明都为局部变量，即仅在函数内可见。
2. 全局作用域
定义在python模块文件中的变量名拥有全局作用域，需要注意的是，这里的全局仅限单个文件，即
在一个文件的顶层的变量名仅在这个文件内可见，并非所有的文件，其他文件中想使用这些变量名
必须先导入对应的模块。当在函数之外给一个变量名赋值时是在全局作用域的情况下进行的。
3. 嵌套作用域
一般在多重函数嵌套的情况下才会考虑到。需要注意的是global语句仅针对全局变量，在嵌套作用
域的情况下，如果想在嵌套的函数内修改外层函数中定义的变量，即使使用global也不能达到目的，
其结果最终是在嵌套的函数所在的命名空间中创建了一个新的变量。
4. 内置作用域
它是通过一个标准库名为__builtin__的模块来实现的。

名字查找机制：
1. 在最内层的范围内查找，一般而言，就是函数内部，即在locals()里面查找。
2. 在模块内查找，即在globals()里面查找。
3. 在外层查找，即在内置模块中查找，也就是在__builtin__中查找。
'''
a2 = 1
def func_56():
    var = 'a'
    def inner():
        global var
        var = 'b'
        print('inside inner, var is ', var)
    inner()
    print('outside, var is ', var)
    
    def foo():
        a = 1
        def bar():
            b = a * 2   # 行不通
            # 在CPython实现中，只要出现了赋值语句，那么这个名字就被当作局部变量看待
            # 上面先执行a * 2，查找a的时候没有，就抛出UnboundLocalError错误。
            # 在python2中可以在函数外实现定义一个全局变量，然后在读写（包括只是访问）
            # 该变量的作用域中都要先使用global声明其为全局变量。
            a = b + 1
            print(a)
        return bar
    
    def foo2(x):
        global a2
        a2 *= x
        def bar():
            global a2
            b = a2 * 2
            a2 = b + 1
            print(a2)
        bar()
        print(a2)
    # 此外也可以将a2作为foo2()里面的一个容器来声明，也可以达到目的。但是使用global全局
    # 变量不提倡，使用容器也不太好，真正的解决方案是python3的nonlocal关键字。
    def foo3():
        a = 10
        def bar():
            nonlocal a
            a *= 10
            print(a)
        bar()
        print(a)
    
#     foo()()
#     foo2(1)
    foo3()


# 建议57：为什么需要self参数
# 略。


# 建议58：理解MRO与多继承
# 新式类广度C3 MRO算法
class Base(object):
    def __init__(self):
        print("enter Base")
        print("leave Base")
 
class A(Base):
    def __init__(self):
        print("enter A")
        super(A, self).__init__()
        print("leave A")
 
class B(Base):
    def __init__(self):
        print("enter B")
        super(B, self).__init__()
        print("leave B")
 
class C(A, B):
    def __init__(self):
        print("enter C")
        super(C, self).__init__()
        print("leave C")
        
def func_58():
    C()
    print(C.mro())
'''
super和父类没有实质性的关联。
通过C类的mro()或者__mro__，我们看到：
<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, 
<class '__main__.Base'>, <class 'object'>
一个类的MRO列表就是合并所有父类的MRO列表，并遵循以下三条原则：
1. 子类永远在父类前面
2. 如果有多个父类，会根据它们在列表中的顺序被检查
3. 如果对下一个类存在的两个合法的选择，选择第一个父类
super的工作原理如下：
def super(cls, inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]
所以上面的调用中super中mro一直都是C的对象，这样才得到了上面的结果。
'''


# 建议59：理解描述符机制
'''

'''


# 建议60：区别__getattr__()和__getattribute__()方法
'''
__getattr__()：属性不在__dict__中；属性不在其基类以及祖先类的__dict__中；触发
AttributeError异常时（注意，不仅仅是__getattribute__()引发的AttributeError异常，
property中定义的get()方法抛出异常的时候也会调用该方法）。
需要特别注意的是当这两个方法同时被定义的时候，要么在__getattribute__()中显式调用，
要么触发AttributeError异常，否则__getattr__()永远不会被调用。
注意事项：
1. 注意无穷递归调用
覆盖__getattr__()和__getattribute__()的时候必须小心，调用父类的相应方法才不会造成无穷
递归。
2. 访问未定义的属性。如果在__getattr__()方法中不抛出AttributeError异常或者显式返回一个
值，则会返回None，此时可能会影响程序的实际运行预期。
'''
def func_60():
    class BBC(object):
        def __init__(self, name):
            self.name = name
            self.x = 20
            
        def __getattr__(self, name):
            print('calling __getattr__:', name)
            if name == 'z':
                return self.x ** 2
            elif name == 'y':
                return self.x ** 3
#             raise AttributeError    # 抛出其他异常将捕捉不到
            
        def __getattribute__(self, attr):
            try:
                return super(BBC, self).__getattribute__(attr)
            except KeyError:
                return 'default'
    
    a = BBC('attribute')
    print(a.name)
    print(a.z)
    if hasattr(a, 't'):
        c = a.t
        print(c)
    else:
        print('instance a has no attribute t')
    '''
    用户本来的意图是：如果t不属于实例属性，则打印出警告信息，否则给c赋值，但实际却输出None。
    这是因为在__getattr__()方法中没有抛出任何异常也没有显式返回一个值，None被作为默认值
    返回并动态添加了属性t，因此hasattr(object, name)的返回结果为True。如果我们在上述
    例子中抛出异常（raise TypeError('unknow attr:' + name)）（NO），则一切如愿。
    两点提醒：
    1. 覆盖了__getattribute__()方法之后，任何属性的访问都会调用用户定义的__getattribute__()
    方法，性能上有所降低，比使用默认的方法要慢。
    2. 覆盖的__getattr__()方法如果能够动态处理事先未定义的属性，可以更好地实现数据
    隐藏。因为dir()通常只显示正常的属性和方法，因此不会将该属性列为可用属性。上面例子中
    如果动态添加属性y，即使hasttr(a, 'y')的值为True，dir(a)得到的属性中却没有y属性。
    '''
        
        
# 建议61：使用更为安全的property
'''
property的定义为：
property(fget=None, fset=None, fdel=None, doc=None)
值得注意的是，使用property并不能真正地实现完全属性只读的目的，正如以双下划线命名的变量
并不是真正的私有变量一样，这些方法只是在直接修改属性上增加了一些障碍。
'''
def func_61():
    class Some_Class(object):
        def __init__(self):
            self._somevalue = 0
            
        def get_value(self):
            print('calling get method to return value')
            return self._somevalue
        
        def set_value(self, value):
            print('calling set method to set value')
            self._somevalue = value
            
        def del_attr(self):
            print('calling delete method to delete value')
            del self._somevalue
        x = property(get_value, set_value, del_attr, "I'm the 'x' property.")
        
    class Some_Class2(object):
#         _x = None
        def __init__(self):
            self._x = None
            
        @property
        def x(self):
            print('calling get method to return value')
            return self._x
        
        @x.setter
        def x(self, value):
            print('calling set method to set value')
            self._x = value
            
        @x.deleter
        def x(self):
            print('calling delete method to delete value')
            del self._x
        
#     obj = Some_Class()
    obj = Some_Class2()
    obj.x = 10
    print(obj.x + 2)
    del obj.x
    obj.x
    

# 建议62：掌握metaclass


# 建议63：熟悉python对象协议


# 建议64：利用操作符重载实现中缀语法
# pipe库


# 建议65：熟悉python迭代器协议
class Iter(object):
    def __init__(self):
        self.idx = -1
        self.items = [12, 9, 0, 8, -2]
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.idx += 1
            return self.items[self.idx]
        except IndexError:
            self.idx = -1
            raise StopIteration

def func_65():
    a = Iter()
    for i in a:
        print(i)
        
        
# 建议66：熟悉python的生成器


# 建议67：基于生成器的协程及greenlet
'''
greenlet是一个C语言编写的程序库，它与yield没有密切的关系。greenlet这个库里最为关键
的一个类型就是PyGreenlet，它是一个结构体，每一个PyGreenlet都可以看到一个调用栈，从
它的入口函数开始，所有的代码都在这个调用栈上运行。它能够随时记录代码运行现场，并随时
中止，以及恢复。
'''
from greenlet import greenlet
def func_67():
    def test1():
        print(12)
        gr2.switch()
        print(34)
        
    def test2():
        print(56)
        gr1.switch()
        print(78)
        
    gr1 = greenlet(test1)
    gr2 = greenlet(test2)
    gr1.switch()
#     gr2.switch()
    # 最后一行跳到test1，输出12，跳到test2，输出56，跳回test1，输出34；然后test1执行
    # 完，gr1就死了。然后，最初的gr1.switch()调用返回，所以永远也不会输出78。
    # gevent将greent与libevent/libev结合起来，时下最受欢迎的网络编程库。


# 建议68：理解GIL的局限性
'''
全局解释器锁
它是python虚拟机上用作互斥线程的一种机制，它的作用是保证任何情况下虚拟机只有一个线程被
运行，而其他线程都处于等待GIL锁被释放的状态。
对于有I/O操作的多线程，始终只有一个活的了GIL锁的线程在运行，每次遇到I/O操作便会进行
GIL锁的释放；但对于纯计算的程序，没有I/O操作，解释器便会根据sys.setcheckinterval的设置
来自动进行线程间的切换，默认情况下每个100个时钟（python内部时钟，对应于解释器执行的
指令）就会释放GIL锁从而轮换其他线程的执行。
好处：大大简化了python线程中共享资源的管理，此外，对于扩展的C程序的外部调用，即使不是
线程安全的，但由于GIL的存在，线程会阻塞直到外部调用函数返回，线程安全不再是一个问题。
'''


# 建议69：对象的管理与垃圾回收

        


if __name__ == '__main__':
    func_55()
#     func_56()
    # func_58()
#     func_60()
#     func_61()
#     func_65()
#     func_67()
    