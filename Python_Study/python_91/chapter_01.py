#!usr/bin/env python
#coding:utf-8


# 建议1：理解pythonic概念
'''
1. 字符串推荐format占位匹配。
2. revered。
3. for循环迭代。
4. with打开文件。
5. 库框架潮流
    A. 包和模块的命名采用小写、单数形式，而且短小。
    B. 包通常仅作为命名空间，如只包含空的__init__.py文件。
'''


# 建议2：编写pythonic代码
'''
1. 避免劣化代码
    A. 避免只用大小写来区分不同的对象。
    B. 避免使用容易引起混淆的名称。
    C. 不要害怕过长的变量名。
2. 深入认识python有助于编写pythonic代码
    A. 全面掌握python提供给我们的所有特性，包括语言特性和库特性。
    B. 随着python的更新要不断更新python知识。
    C. 深入学习业界公认的比较pythonic的代码，比如Flask、gevent和requests等。
    D. 可以采用PEP8规范检查python是否够pythonic。
'''


# 建议3：理解python与C语言的不同之处
'''
C是编译性语言，python是脚本语言，从原理上来说是完全不一样的。
一些语法的不同：
1. 缩进与{}。
2. 单双引号。
3. 三元操作符?:。
python使用x if condition else y来替代。
4. switch case，python没有这个，可以使用if...elif...else来替换，也可以使用跳转表实现：
def f(x):
    return {0: 'NOK', 1: 'OK', 2: 'Go'}.get(x, 'Default')
'''


# 建议4：在代码中适当添加注释


# 建议5：通过适当添加空行使代码布局更为优雅、合理


# 建议6：编写函数的4个原则
'''
1. 函数的设计要尽量短小，嵌套层次不宜过深。
2. 函数名能够正确反映它的大概作用，参数的设计也应该简单明了。
3. 函数的设计应该考虑向下兼容。
4. 一个函数只做一件事，尽量保证函数语句粒度的一致性。
'''

# 建议7：将常量集中到一个文件
'''
python是动态语言，支持的常量很少很少，只有简单的True、False、None等。
1. 通过命名风格来提醒使用者该变量代表的意义为常量，如全部大写。
2. 通过自定义类来实现常量功能.
'''
class const(object):
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstCaseError("Cannot /change const:%s" % name)
        if not name.isupper():
            raise self.ConstCaseError("const name '%s' is not all uppercase" % name)
        self.__dict__[name] = value
import sys
sys.modules[__name__] = const() # 重命名模块，将模块命名为const对象

