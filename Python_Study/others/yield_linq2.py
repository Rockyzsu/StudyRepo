#!urs/bin/env python
#coding:utf-8


# import sys
# sys.setrecursionlimit(1000000)

def make_numbers():
    n = 1
    while True:
        yield n
        n += 1
        
def foo(x):
    return x % 10 == 2

def bar(x):
    return x % 3 == 0

def filter_while(func, stream):
    while True:
        n = next(stream)
        if func(n):
            yield n
        
def run(number):
    stream = make_numbers()
    for _ in range(number):
        stream = filter_while(foo, stream)
        stream = filter_while(bar, stream)
        n = next(stream)
        print(n)
        print(stream)
        
def run2(number):
    stream = make_numbers()
    stream = filter_while(foo, stream)
    stream = filter_while(bar, stream)
    n = 1
    for i in stream:
        print(i)
        n += 1
        if n == number: break

if __name__ == '__main__':
    run(10)
#     run2(10)
    