# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月5日
    @author: xiongqiao
    @attention：
'''



from pipe import *


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def foo1():
    print(range(5) | add)
    
def foo2():
    print(range(5) | where(lambda x: x % 2) | add)
    
def foo3():
    print(fibonacci() | select(lambda x: x ** 2) | take_while(lambda x: x < 100) | as_list)
    
@Pipe
def take_while_idx(iterable, predicate):
    #自定义流处理函数，只需要定义一个生成器函数并加上修饰器Pipe
    #实现了一个获取元素直到索引不符合条件的流处理函数
    for idx, x in enumerate(iterable):
        if predicate(idx):
            yield x
        else:
            return
        
def foo4():
    print(fibonacci() | take_while_idx(lambda x: x < 10) | as_list)
    
def foo5():
    a = [1, 2, 3, 4, 5]
    print(a | concat)       #output string
    print(a | concat('#'))  #output string
    
def foo6():
    a = [[1, 2], [3, 4], [5]]
    print(a | chain)
    print(a | chain | concat)
    
def foo7():
    #groupby()
    a = range(1, 10) | groupby(lambda x: x % 2 and 'Even' or 'Odd')
    for m, n in a:
        print('%s:%s' % (m, str(list(n))))
#     b = a | groupby(lambda x: x % 2 and 'Even' or 'Odd') | \
#     select(lambda x: '%s : %s' % (x[0], (x[1] | concat(',')))) | \
#     concat(' / ')
#     print(b)

def group_normal():
    from itertools import groupby
    def height_class(h):
        if h > 180:
            return "tall"
        elif h < 160:
            return "short"
        else:
            return "middle"

    friends = [191, 158, 159, 165, 170, 177, 181, 182, 190]
    friends = sorted(friends, key = height_class)
    for m, n in groupby(friends, key = height_class):
        print(m)
        print(list(n))



def foo8():
    a = '''GET /HTTP /1.0
    Host: baidu.com
    '''
#     print(a | netcat('baidu.com', 80) | concat | stdout)
#     10 | stdout
#     '10hello\n  my first time.' | lineout
    b = a | netcat('http://www.baidu.com', 80)
    print(b)
    

class MM(object):   
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return self.function(other)

#     def __call__(self, *args, **kwargs):
#         return MM(lambda x: self.function(x, *args, **kwargs))
    
@MM
def add2(x):
    return sum(x)

@MM
def first2(iterable):
    return next(iter(iterable))
    

def main():
    # foo1()
#     foo2()
#     foo3()
#     foo4()
#     foo5()
#     foo6()
#     foo7()
#     group_normal()
#     foo8()
    print(range(10) | add2)
#     print(range(1, 29) | first2)

if __name__ == '__main__':
    main()
