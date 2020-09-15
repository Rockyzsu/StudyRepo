#!urs/bin/env python
#coding:utf-8

import sys
sys.setrecursionlimit(1000000)


# 筛选法求素数序列是这样求的：
# 1、2是素数，将2后面的整数中是2倍数的数删去（过滤）；
# 2、3是素数，将3后面的整数中是3倍数的数删去；
# 3、4在第1步已经被删掉了。5是素数。将5后面的整数中是5倍数的数删去；
# ……
# 重复这个过程，最后留下来的就是素数序列。以流计算模式的思路来看，就是每次取出一个素数p后，
# 就以不整除这个素数p作为过滤条件对后面的流进行过滤


def integers_starting_from(i):
    while True:
        yield i
        i += 1

def stream_filter(func, stream):
    while True:
        x = next(stream)
        if func(x):
            yield x
            
def divisible(x):
    return lambda e: e % x != 0

def f1(x):
    return x % 2 != 0

def f2(x):
    return x % 3 != 0
            
def sieve():
    stream = integers_starting_from(2)
    while True:
        x = next(stream)
        yield x
        stream = stream_filter(
            divisible(x),
#             lambda e: e % x != 0,  # 这里不能用lambda，否则x的值会不对导致过滤错误。
            stream)
        
def sieve2():
    stream = integers_starting_from(2)
    stream = stream_filter(f1, stream)
    stream = stream_filter(f2, stream)
    return stream
        
def printn(n):
    stream = sieve()
    for _ in range(n):
        print(next(stream))
    
def printn2(n):
    stream = sieve2()
    end = 1
    for i in stream:
        print(i)
        end += 1
        if end == n: break
        

# 最开始的流是一个从2开始的整数序列。每次从流中取出一个数x（第一次取出的是2，后面取出的是后继的素数），
# 新建一个过滤条件divisible(x)，用stream_filter过滤这个序列。举个例子：
# 1、第一次调用，返回2，stream变成：{x | x <- [3, 4, ...], x%2 != 0}
# 2、第二次调用，返回3，stream变成：{x | x <- [4, 5, ...], x%2 != 0, x%3 != 0}
# 3、第三次调用，返回5（因为4被过滤了），stream变成：{x | x <- [6, 7, ...], x%2 != 0, x%3 != 0, x%5 != 0}
# ……
# 留下来的只剩素数。下面代码打印前100个素数
 

if __name__ == '__main__':
#     printn(100000)
    printn2(1000)
    