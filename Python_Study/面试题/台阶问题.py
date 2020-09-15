#!usr/bin/env python
#coding:utf-8

from itertools import islice

fib = lambda n: n if n <= 2 else fib(n - 1) + fib(n - 2)

def fib2():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b

if __name__ == '__main__':
    a = fib(5)
    print(a)
    
    for i in islice(fib2(), 0, 10):
        print(i)
