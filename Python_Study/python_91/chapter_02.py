#!usr/bin/env python
#coding:utf-8


# 建议8：利用assert语句来发现问题
'''
assert主要为调试服务，能够快速方便地检查程序的异常或者发现不恰当的输入等。基本语法：
assert expression1 ["," expression2]
当expression1的布尔值为False的时候，引发AssertionError，而expression2是可选的，常用
来传递具体的异常信息。
__debug__这个变量是只读（True）的，而且还不能修改。
断言是有代价的，它会对性能产生一定的影响。对于编译性语言，像C/C++，这也许并不重要，
因为断言只在调试模式下生效。但python并没有严格的调试和发布模式，通常禁用断言的方法
是在运行脚本的时候加上-O标识，这种方式影响是它并不优化字节码，而是忽略与断言相关的语句。

断言实际被设计用来捕获用户所定义的约束的，而不是用来捕获程序本身错误的，因此使用断言
需要注意以下几点：
1. 不要滥用，这是断言最基本的原则。若由断言引发了异常，通常代表程序中存在bug。因此
断言应该用在正常逻辑不可到达的地方或正常情况下总是为真的场合。
2. 如果python本身异常能够处理就不要使用断言，如数组越界、类型不匹配、除数为0之类的错误。
3. 不要使用断言来检查用户的输入。
4. 在函数调用后，当需要确认返回值是否合理时可以使用断言。
5. 当条件是业务逻辑继续下去的先决条件时可以使用断言。
'''
def func_08():
    assert 0, '不能输入布尔值为假的变量！'
    # [我]实际下面这一条已经不会被执行的了
    print('断言已经被忽略掉了！')


# 建议9：数据交换的时候不推荐使用中间变量


# 建议10：充分利用Lazy evaluation的特性（延迟计算）
'''
1. and和or的截断
x and y：如果x为假，那么表达式就为假，不再计算y。
x or y：如果x为真，那么表达式就为真，不再计算y。
2. yield的无限循环。
'''
def func_10():
    # 斐波拉契数列
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def call_func_10():
    from itertools import islice
    # islice(seq, [start,] stop [, step])
    # 0 <= start <= maxsize; step = None or positive integer
    print(list(islice(func_10(), 5)))

    a = [23, 0, 9, 8, 22, 11]
    print(list(islice(a, 1, 4, -2)))


# 建议11：理解枚举替代实现的缺陷
# python3.4之前并不提供枚举类型
from enum import Enum, unique
def func_11():
    Months = Enum('Moths', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                            'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
                  )
    for name, member in Months.__members__.items():
        print(name, '=>', member, ',', member.value)
    # value属性是自动赋给成员的int常量，默认从1开始

# 如果要更精确地控制枚举类型，可以从Enum派生出自定义类型：
# unique装饰器可以帮助我们检查保证没有重复值
@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
#     De = 6  # 重复一个值不能通过

def func_11_02():
    for name, member in Weekday.__members__.items():
        print(name, '=>', member, ',', member.value)

    # 修改一个值试试
#     Weekday.Sun.value = 10  # AttributeError:can't set attribute


# 建议12：不推荐使用type来进行类型检查
class UserInt(int):
    def __init__(self, val=0):
        self._val = int(val)

    def __add__(self, val):
        if isinstance(val, UserInt):
            return UserInt(self._val + val._val)

    def __iadd__(self, val):
        raise NotImplementedError('not support operation')

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return 'Integer(%s)' % self._val


def func_12():
    n = UserInt()
    print(n)
    m = UserInt(2)
    print(m)
    print(n + m)
    print(type(n) is int)   # False
    print(isinstance(n, int))   # True
    # 从输出结果来看，type()函数认为n不是int类型，但实际上它是，显然是不合理的。
    # 由此可见基于内建类型扩展的用户自定义类型，type函数并不能准确地返回结果。


# 建议13：尽量转换浮点类型后再做除法
# 这个问题在python3中已经得到解决
def func_13():
    i = 1
    while i != 1.5: # 要避免这种表达式
        i += 0.1
        print(i)
    # 这段代码会导致无限循环
    # 在计算机的世界里，浮点数的存储规则决定了不是所有浮点数都能准确表示，有些是不准确
    # 的，只是无限接近。在内存中根据浮点数位数规定，多余部分直接截断，因此当循环到第五
    # 次的时候，i的实际值为1.50000 0000 0000 004，则条件表达式i != 1.5仍然为True，
    # 循环陷入无限循环。
    # 对于浮点数的处理，其计算结果并不是完全准确的。如果计算精度要求较高，可以使用
    # Decimal来进行处理或者将浮点数尽量扩大为整数，计算完毕后再转换回去。


# 建议14：警惕eval()的安全漏洞
'''
eval(expression[, globals[, locals]])
参数globals为字典形式，locals为任何映射对象，它们分别表示全局和局部命名空间。如果传入
globals参数的字典中缺少__builtins__的时候，当前全局命名空间将作为globals参数输入并且
在表达式计算之前被解析。locals参数默认与globals参数相同，如果两者都省略的话，表达式
将在eval()调用的环境中进行。
参数globals是全局命名空间，可以指定执行表达式时的全局作用域的范围，比如指定某些模块可
以使用。如果本参数缺省，就使用当前调用这个函数的当前全局命名空间；参数locals是局部作
用域命名空间，是用来指定执行表达式时访问的局部命名空间。如果全局命名空间参数出现，但
缺省内置模块，那么会自动拷贝这个模块到全局命名空间，意味着无论怎么设置，都可以使用内
置模块。如果两个命名空间，都使用缺省方式，就会使用调用这个函数时的命名空间来查找相应
的变量。
'''
from math import *
def func_14():
#     eval(__import__('os').system('dir'))    # 参数错误也会执行里面的语句
#     eval("__import__('os').system('dir')")

    def exp(string):
        # 在globals参数中禁止全局命名空间的访问
        try:
            math_fun_list = ['acos', 'asin', 'atan', 'cos', 'e', 'log', 'log10',
                             'pi', 'sin', 'sqrt', 'tan']
            math_fun_dict = dict([(k, globals().get(k)) for k in math_fun_list])
            print(math_fun_dict)
            print('Your answer is', eval(string, {'__builtins__': None}, math_fun_dict))
            while 1: pass
        except NameError:
            print('The expression you enter is not valid.')
#     exp('sin(0.5)')     # OK
#     exp('round(10.0)')  # 本来是可以执行的，由于globals的被屏蔽了，现在也执行不了了
    exp("__import__('os').system('dir')")   # 现在这个能屏蔽掉了
    # 直接导致程序退出，假如我有个服务器，那么就宕机了。
    exp('[c for c in "".__class__.__bases__[0].__subclasses__() if c.__name__=="Quitter"][0](0, "")()')

def func_14_02():
    # 安全的方式
    import ast
    ast.literal_eval("__import__('os').system('dir')")


# 建议15：使用enumerate()获取序列迭代的索引值
# enumerate(sequence, start=0)
# enumerate(sequence, start=0)的内部实现实际相当于如下代码：
def enumerate_(seq, start=0):
    n = start
    for elem in seq:
        yield n, elem
        n += 1


# 建议16：分清==与is的适用场景
'''
1. ==
==表示两个变量的值是否相等
2. is
is表示两个变量是否是同一个变量

==实际上是调用的__eq__()方法，因此a==b实际是调用的a.__eq__(b)，所以==可以被重载，但是
is不行。一般情况下，如果x is y是True，那么x == y也是True（特殊情况除外，如NaN，a = float('NaN')，
a is a为True，a == a为False），反之则不然。
'''
def func_16():
    a = float('NaN')
    print(a is a)
    print(a == a)


# 建议17：考虑兼容性，尽可能使用unicode
# 在python3中，统一为了unicode，只有byte和string两种类型


# 建议18：构建合理的包层次来管理module
'''
在包目录下有一个__init__.py文件，一般这个文件为空。可以在该文件中申明模块级别的import
语句，从而使其变成包级别可见。假如包Package下Module中的有类Test，普通的时候要使用Test
的时候需要这样：
from Package.Module import Test
我们可以在__init__.py文件中加入：from Module import Test语句，则可以直接使用from Package
import Test语句来导入类Test。如果__init__.py文件为空，当意图使用from Package import *
将包Package中的所有模块导入当前命名空间时并不能使得导入的模块生效，这是因为不同平台间的
文件的命名规则不同，python解释器并不能正确判定模块在对应平台该如何导入，因此它仅仅执行
__init__.py文件。如果要控制模块的导入，则需要对__init__.py文件做修改。
__init__.py文件还有一个作用就是通过在该文件中定义__all__.py变量，控制需要导入的子包
或者模块。现在在Package包中的__init__.py文件中添加：
__all__ = ['Module1', 'Module2', 'Subpackage']
之后再运行from Package import *，那么就可以导入__all__变量中的所有模块了。
'''


if __name__ == '__main__':
    func_08()
#     call_func_10()
#     func_11()
#     func_11_02()
#     func_12()
#     func_13()
#     func_14()
#     func_14_02()
#     func_16()
