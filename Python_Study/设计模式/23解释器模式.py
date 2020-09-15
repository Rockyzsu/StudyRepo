#!urs/bin/env python
#coding:utf-8


# 解释器模式：给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该
# 表示来解释语言中的句子。[DP]
# 如果一种特定类型的问题发生的频率足够高，那么可能就值的将该问题的各个实例表述为一个简单
# 语言中的句子。这样就可以构建一个解释器，该解释器通过解释这些句子来解决该问题[DP]。

from abc import ABCMeta, abstractmethod

class AbstractExpression(metaclass=ABCMeta):
    # 抽象表达式，声明一个抽象的解释操作，这个接口为抽象语法树中所有的节点所共享。
    @abstractmethod
    def Interpret(self, context): return
    
    
class TerminalExpression(AbstractExpression):
    # 终结符表达式，实现与文法中的终结符相关联的解释操作。实现抽象表达式中所要求的接口，
    # 主要是一个Interpret()方法。文法中每一个终结符都有一个具体终结表达式与之相对应。
    def Interpret(self, context):
        print('终端解释器')
        
        
class NonterminalExpression(AbstractExpression):
    # 非终结符表达式，为文法中的非终结符实现解释操作。对文法中每一条规则R1、R2...Rn
    # 都需要一个具体的非终结符表达式。通过实现抽象表达式的interpret()方法实现解释操作。
    # 解释操作以递归方式调用上面所提到的代表R1、R2...Rn中各个符号的实际变量。
    def Interpret(self, context):
        print('非终端解释器')
        
        
class Context(object):
    # Context类，包含解释器之外的一些全局信息。
    def __init__(self):
        self.input = ''
        self.output = ''
        
        
def run():
    context = Context()
    l = []
    l.append(TerminalExpression())
    l.append(NonterminalExpression())
    l.append(TerminalExpression())
    l.append(TerminalExpression())
    
    [i.Interpret(context) for i in l]
        
if __name__ == '__main__':
    run()