#!usr/bin/env python
#coding:utf-8


# 建议19：有节制地使用from...import语句
'''
python提供了三种方式来导入外部模块：import语句、from...import...及__import__函数。
__import__函数与import语句类似，不同点在于前者显式地将模块的名称作为字符串传递并赋值
给命名空间的变量。
在导入模块的时候，尽量遵循以下几点：
1. 一般情况下优先使用import a形式。
2. 有节制地使用from a import B形式。
3. 尽量避免使用from a import *，因为这会污染命名空间，并且无法清晰地表示导入了哪些对象。

python在初始化运行环境的时候会预先加载一批内建模块到内存中，这些模块相关的信息被存放在
sys.modules中。当加载一个模块时，解释器实际上要完成以下动作：
1. 在sys.modules中搜索看看该模块是否已经存在，如果存在，则将其导入到当前局部命名空间，
加载结束。
2. 如果在sys.modules中找不到对应模块的名称，则为需要导入的模块创建一个字典对象，并将
该对象信息插入sys.modules中。
3. 加载前确认是否需要对模块对应的文件进行编译，如果需要则先进行编译。
4. 执行动态加载，在当前模块的命名空间中执行编译后的字节码，并将其中所有的对象放入模块
对应的字典中。
'''
import sys
def func_19():
    print(dir())
    import test 
    print(dir())    # import test之后局部命名空间发生变化
    print('test' in sys.modules.keys())
    print(dir(test))
    # 需要注意的是，直接使用import和使用from a import B形式这两者之间存在一定的差异，
    # 后者直接将B暴露于当前局部空间，而将a加载到sys.modules集合。

'''
无节制地使用from a import ...会导致一些问题：
1. 命名空间的冲突
一般来说在非常明确不会造成命名冲突的前提下，以下几种情况可以考虑使用：
A. 当只需要导入部分属性或方法时。
B. 模块中的这些属性和方法访问频率较高导致使用 “模块名.名称”的形式进行访问过于繁琐时。
C. 模块的文档明确说明需要使用from...import形式，导入的是一个包下面的子模块，且使用
from...import形式能够更为简单和便利时。
2. 循环嵌套导入的问题
c1.py:
from c2 import g
def x(): pass

c2.py:
from c1 import x
def g(): pass
无论运行那个文件都会导致ImportError异常。
因为在执行c1.py的加载过程中，需要创建新的模块对象c1然后执行c1.py所对应的字节码。此时
遇到语句from c2 import g，而c2在sys.modules也不存在，故此时创建与c2对应的模块对象并
执行c2.py所对应的字节码。当遇到c2中的语句from c1 import x时，由于c1已经存在，于是
便去其所对应的字典中查找g，但c1模块对象虽然创建但初始化的过程并未完成，因此其对应的字典
中并不存在g对象，此时便抛出ImportError异常。而解决循环嵌套导入的问题的一个方法是直接
使用import语句。
'''


# 建议20：优先使用absolute import来导入模块
'''
python2.6以及python3之后默认都是绝对导入，已经不再默认是相对导入了。
'''    
    
    
# 建议21：i+=1不等于++i
'''
python不支持后自增（减）操作，只支持“前自增（减）”操作，但是python仅仅把它认为是正负
号的叠加使用，而不会去真正的进行加减操作。
'''


# 建议22：使用with自动关闭资源
'''
with的语法为：
with 表达式 [as 目标]: 代码块
with支持嵌套，支持多个with子句，它们两者之间可以互相转换。“with expr1 as e1, expr2 as e2”
等于下面的形式：
with expr1 as e1:
    with expr2 as e2:
    
with代码块的执行过程如下：
1. 计算表达式的值，返回一个上下文管理器对象。
2. 加载上下文管理器对象的__exit__()方法以备后用。
3. 调用上下文管理器对象的__enter__()方法。
4. 如果with语句中设置了目标对象，则将__enter__()方法的返回值赋给目标对象。
5. 执行with中的代码块。
6. 如果步骤5中的代码正常结束，调用上下文管理器对象的__exit__()方法，其返回值直接忽略。
7. 如果步骤5中代码执行过程中发生异常，调用上下文管理器对象的__exit__()方法，并将其
异常类型、值及traceback信息作为参数传递给__exit__()方法。如果__exit__()返回值为false，
则异常被重新抛出；如果为true，异常被挂起，程序继续执行。
在测试中return False之后异常并没有被重新抛出。

实现上下文管理器协议：
1. __enter__()：进行运行时的上下文，返回其运行时上下文相关的对象，with语句中会将这个
返回值绑定到目标对象。
2. __exit__(exception_type, exception_value, traceback)：退出运行时的上下文，定义在
块执行（或终止）之后上下文管理器应该做什么。它可以处理异常、清理现场或者处理with块中
语句执行完成之后需要处理的动作。
''' 
class Func_22(object):
    def __enter__(self):
        print('entering...')
        # 目标对象为None
    
    def __exit__(self, exception_type, exception_value, traceback):
        print('leaving...')
        if not exception_type:
            print('no exceptions!')
            return False
        elif exception_type is ValueError:
            print('value error!')
            return True
        else:
            print('other error')
            return True

def func_22():
    with Func_22() as f:
        print(type(f))
        print('Testing...')
#         raise(ValueError)
        raise

# 可以直接使用contextlib中的contextmanager作为装饰器来提供一种针对函数级别上的上下文
# 管理机制，可以直接作用于函数/对象上。
from contextlib import contextmanager
@contextmanager
def func_22_02():
    print('this is a context function.')
    yield   # 必须是一个迭代器
    print('over!')
        
        
# 建议23：使用else子句简化循环（异常处理）
'''
else还可以用在循环中，在for/while中，如果循环没有break跳出语句或者正常执行完，那么else
子句将会被执行。
'''
def func_23():
    for i in range(10):
        if i > 8:
            print('for条件找到，不执行else子句')
            break
    else:
        print('for条件不成立或者循环完毕。')
        
    n = 0
    while n < 10:
        n += 1
    else:
        print('while条件不成立或者循环完毕。')
        
        
# 建议24：循环异常处理的几点基本原则
'''
1. 注意异常的粒度，不推荐在try块中放入过多的代码。
2. 谨慎使用except语句处理所有的异常，最好能定位具体的异常。
3. 注意异常捕获的顺序，在合适的层次处理异常。
推荐的方法是将继承机构中子类异常在前面的except语句中抛出，而父类异常在后面的except语句
中抛出。
另外，如果异常能够在被捕获的位置处理，那么就应该及时处理，不能处理的也应该以合适的方式
向上层抛出。遇到异常不论好歹就向上抛出是不明智的。向上层抛出异常的时候需要注意异常丢失
的情况，可以使用不带参数的raise来传递。
4. 使用更为友好的一场新，遵循异常参数规范。给用户看的异常一定要是用户能明白的异常。
'''
def func_24():
    try:
        raise(UnicodeDecodeError('pdfdocencoding', b'a', 2, -1, 'not support decoding'))
    except ValueError:
        print('ValueError occured') # 这个异常先抛出，掩盖了真正的UnicodeDecodeError错误
    except UnicodeDecodeError as e:
        print(e) 
        
def func_24_02():
    try:
        1 / 0
    except:
        raise   # 向上抛出异常ZeroDivisionError
    
    
# 建议25：避免finally中可能发生的陷阱
def func_25():
    while True:
        try:
            print('I am running...')
            raise(IndexError('r'))
        except NameError as e:
            print('NameError happended %s', e)
            break
        finally:
            print('finally executed')
            break
    # IndexError向上层抛出，但是异常最终没有抛出到调用者一方（丢失）。这是因为当try
    # 块中发生异常的时候，如果在except语句中找不到对应的异常处理，异常将被保存起来。
    # 当finally执行完毕的时候，临时保存的异常将会再次被抛出。但是如果finally中产生了
    # 新的异常或者执行了break或者return语句，那么临时保存的异常将会丢失，从而导致异常
    # 的丢失。
    
def func_25_02(a):
    try:
        if a <= 0:
            raise ValueError('data cannot be negative')
        else: return a
    except ValueError as e:
        print(e)
    finally:
        print('The end!')
        return -1
    # func_25_02(0)和func_25_02(2)都会返回-1。func_25_02(2)在执行的时候，if条件不通过，
    # 执行else条件，但是在执行else条件之前要先执行finally语句，直接就返回-1了。
    
    
# 建议26：深入理解None，正确判断对象是否为空
class Func_26(object):
    def __bool__(self):
        print('bool')
        return True
    
    def __len__(self):
        print('get length')
        return False
# __nonzero__()方法：对自身对象进行空值测试，返回0/1或者True/False。如果一个对象没有
# 定义该方法，python取__len__()方法调用的结果来进行判断。__len__()返回0则表示空。如果
# 一个类中既没有定义__nonzero__()也没有定义__len__()方法，该类的实例用if判断都是True。
# 在python3中移除了__nonzero__()方法，并使用__bool__()替代。
    
def func_26():
    if Func_26():
        print('not empty')
    else:
        print('empty')
#     print(bool(Func_26()))


# 建议27：连接字符串应优先使用join而不是+

import timeit
strlist = ['it is a long value string will not keep in memory' for n in range(100000)]
def join_test():
    return ''.join(strlist)
def plus_test():
    result = ''
    for _, v in enumerate(strlist):
        result += v
    return result

def func_27():   
    jointimer = timeit.Timer('join_test()', 'from __main__ import join_test')
    print(jointimer.timeit(number=100))
    plustimer = timeit.Timer('plus_test()', 'from __main__ import plus_test')
    print(plustimer.timeit(number=100))
'''
用操作符+连接字符串的时候，由于字符串是不可变对象，其工作原理实际是这样的：如果要连接
S1+S2+...+Sn，执行一次+操作便会在内存中申请一块新的内存，并将上一次操作的结果和本次操作
的右操作数复制到新申请的内存中。即当S1+S2的时候会申请一块内存，并将S1、S2复制到该内存
中。依此类推，相当于S1被复制了n-1次，S2被复制n-2次...Sn被复制1次（并不完全等同于S1复制
n-1次，因为后续复制都是对中间结果的复制），所以字符串的连接时间约为s*n^2，其中s为复制
依此字符串的平均时间。
而用join()的时候，计算机直接计算需要申请的总内存空间，然后一次性申请那么多并将字符序列
中的每一个元素复制到内存中去，所以join操作的时间约为s*n。
'''
    
    
# 建议28：格式化字符串尽量使用format()方式，而不是%
def func_28():
    # 1. 直接格式化字符或者数值
    print('your score is %06.1f' % 9.5)
    # 2. 元组形式格式化
    print('%d plus %d is 10.' % (4, 6))
    # 3. 字典形式格式化
    d = {'first': 'hello', 'second': 1}
    print('You said:"%(first)s %(second)d"' % d)
    
    # format的基本语法是：[[填充符] 对齐方式] [符号] [#] [0][宽度][,][.精确值][转换类型]
    # 其中填充符可以是除了{、}符号之外的任意符号。
    '''
    对齐方式：
    <    表示左对齐，大多数对象为默认的对齐方式。
    >    表示右对齐，数值默认的对齐方式。
    =    仅对数值型有效，如果有符号的话，在符号后数值前进行填充，如-000029。
    ^    居中对齐，用空格进行填充。
    
    符号：
    +    正数前加+，负数前加-。
    -    正数前不加符号，负数前加-，为数值的默认形式。
    空格    正数前加空格，负数前加-。
    '''
    # 1. 直接使用位置符号
    print('my name is {0}, hello {1}'.format('Jack', 'Tom'))
    # 2. 使用名称
    print('my name is {name}, hello {you}'.format(name='Jack', you='Tom'))
    # 3. 通过属性
    class A():
        def __init__(self):
            self.me = 'Boss'
            self.you = 'staff'
            print('I am {self.me}, you are {self.you}'.format(self=self))
    A()
    # 4. 格式化元组的具体项
    point = (1, 3)
    print('X:{0[0]}; Y:{0[1]}'.format(point))
    # 另外一个例子
    w =[('a', 1), ('b', 20), ('c', 0)]
    f = 'this is {0[0]}, this is {0[1]}'.format
    for i in map(f, w):
        print(i)
        

# 建议29：区别对待可变对象和不可变对象
'''
python一切皆对象，每一个对象都有一个唯一的标识符、类型以及值。对象根据其值是否能修改
分为可变对象和不可变对象。其中数字、字符串、元组属于不可变对象，字典、列表和数组属于
可变对象。
'''
def func_29():
    def foo(n, a=[]):
        a.append(n)
        return a
    a = foo(10)
    print(a)
    b = foo(20)
    print(b)
    # 上面会输出[10]，然后是[10,20]
    # 默认参数在被调用的时候仅仅被评估一次，以后都会用第一次评估的结果，如果是可变对象
    # 的话，那么一直就是那一个可变对象。
    
    # 对于可变对象，还有一个问题是要注意的：
    list1 = ['a', 'b', 'c']
    list2 = list1
    list1.append('d')
    print(list1)
    print(list2)    # list2也会发生变化
    list3 = list1[:]    # 切片相当于浅复制
    list3.remove('a')
    print(list3)
    print(list1)
    print(list2)
    print(id(list3))    # 重新指向一块内存
    print(id(list1))
    print(id(list2))
    
    
# 建议30：[]、{}和()：一致的容器初始化形式
def func_30():
    words = ['  Are', ' abandon', 'Passion', 'Business', ' fruit  ', 'quit']
    print([i.strip() for i in words if i.strip().istitle()])
    list2 = [['Hello', 'World'], ['goodbye', 'Jack']]
    print([[j.upper() for j in i] for i in list2])  # 多重嵌套
    print([(a, b) for a in [1, 4, 3] for b in [2,10, 9]])   # 多重迭代
    # 元组的初始化语法为：
    # (expr for iter_item in iterable if cpnd_expr)
    # 类似地，集合、字典也有类似的语法
    # 此外，当函数接受一个可迭代对象参数时，可以使用元组的简写方式
    def foo(a):
        for i in a: print(i, end=' ')
    foo([1, 2, 3])
    print()
    foo(i for i in range(3) if i % 2 == 0)  # 省略方括号
    
    
# 建议31：记住函数传参既不是传值也不是传引用
# 可变对象传引用，不可变对象传值，这是不对的。
def func_31():
    def change_me(org_list):    
        print(id(org_list))
        new_list = org_list
        print(id(new_list))
        if len(new_list) > 5:
            new_list = ['a', 'b', 'c']
        for i, e in enumerate(new_list):
            if isinstance(e, list):
                new_list[i] = '***'
        print(new_list)
        print(id(new_list))
    
    test1 = [1, ['a', 1, 3], [2, 1], 6]
    change_me(test1)
    print(test1)
    
    test2 = [1, 2, 3, 4, 5, 6, [1]]
    change_me(test2)
    # 长度大于5的时候，new_list = ['a', 'b', 'c']操作重新创建了一块内存并将new_list
    # 指向它。而传入的test2并没有改变。
    print(test2)
    '''
    正确的叫法应该是叫传对象或者说传对象引用。函数参数在传递过程中将整个对象传入，对可变
    对象的修改在函数外部以及内部可见，调用者和被调用者之间共享这个对象。而对于不可变对象，
    由于并不能被真正被修改，因此，修改往往是通过生成一个新对象然后赋值来实现。
    '''
    
    
# 建议32：警惕默认参数潜在的问题
def func_32(item, list_=[]):
    print(id(list_))
    list_.append(item)
    print(id(list_))
    print(list_)
    # def在python中是一个可执行语句，当解释器执行def的时候，默认参数也会被计算。
    import time
    def timer(when=time.time()):    # 正确方式应该是when=time.time
        print('now is %s', when)    # when()
    
    timer()
    time.sleep(1)
    timer()
    
    
# 建议33：慎用变长参数
# 略


# 建议34：深入理解str()和repr()的区别
'''
1. 两者之间的目标不同：str()主要面向用户，其目的是可读性，返回形式为用户友好性和可读性
都较强的字符串类型；而repr()面向的是python解释器，或者说开发人员，其目的是准确性，其
返回值表示python解释器内部的含义，常作为编程人员debug用途。
2. 在解释器中直接输入a时默认调用repr()函数，而print(a)则调用str()函数。
3. repr()的返回值一般可以用eval()函数来还原对象，通常有如下等式：
obj == eval(repr(obj))
但它并不是在所有情况下都成立，比如在用户重新实现repr()。
4. 这两个方法分别调用内建的__str__()和__repr__()方法，一般来说在类中都应该定义__repr__()
方法，而__str__()方法则为可选，当可读性比准确性更为重要的时候应该考虑定义__str__()方法。
如果类中没有定义__str__()方法，则默认会使用__repr__()方法的结果来返回对象的字符串表示
形式。用户返回__repr__()方法的时候最好保证其值可以用eval()方法使对象重新还原。
'''
def func_34():
    s = "' '"
    print(s)
    print(repr(s))
    print(eval(repr(s)) == s)
    eval(str(s))
    print(eval(str(s)) == s)
    
    class A(object):
        def __init__(self, a):
            self.a = a
        
        def __repr__(self, *args, **kwargs):
            return self.a
    
    a = A('你是我的小苹果')
    print(a)
    
    
# 建议35：分清classmethod和staticmethod的适用场景
'''
1. 静态方法
a. 静态方法定义在类中，较之外部函数，能够更加有效地将代码组织起来，从而使相关代码的垂直
距离更近，提高代码的维护性。
b. 如果有一组独立的方法，将其定义在一个模块中，通过模块来访问这些方法也是一个不错的选择。
2. 类方法
类方法的调用使用类本身作为其隐含参数，但调用本身并不需要显式提供该参数。
'''
class Fruit(object):
    total = 0
    @classmethod
    def print_total(cls):
        print(cls.total)
        print(id(Fruit.total))
        print(id(cls.total))
    
    @classmethod
    def set(cls, value):
        print('calling class_method(%s, %s)' % (cls, value))
        cls.total = value   # 动态的类变量
        
class Apple(Fruit): None
class Orange(Fruit): None

def func_35():
    app1 = Apple()
    app1.set(200)
    org1 = Orange()
    org1.set(300)
    app1.print_total()  # 200
    org1.print_total()  # 300
# 动态地生成了对应类的类变量，这就是classmethod的妙用。


        
        
    
if __name__ == '__main__':
#     func_19()
#     func_22()
#     with func_22_02(): pass
#     func_23()
#     func_24()
#     func_24_02()
#     func_25()
#     print(func_25_02(0))
#     print(func_25_02(2))
#     func_26()
#     func_27()
#     func_28()
#     func_29()
#     func_30()
#     func_31()
#     func_32(2, ['2', 'c'])
#     func_34()
    func_35()
