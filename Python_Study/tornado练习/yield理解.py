# !/usr/bin/python
#coding:utf-8


def loop1():
    """ 循环1负责抛出一个函数和对应的参数, 并接收结果
    """
    a = 0
    ret = 1
    while True:
        ret = yield sum, [a, ret]   # 须输入，“返回”数据
        a, ret = ret, a
        print("Loop1 ret", ret)
        
        
def loop2():
    """ 循环2 负责接收函数并计算结果, 然后 yield 出结果
    """
    while True:
        func, args = yield  # 须输入，不“返回”数据
        yield func(args)    # 不接受输入，“返回”数据
 

def run1():
    l1 = loop1()
    l2 = loop2()
    tmp = next(l1)
     
    for _ in range(10):
        next(l2)
        ret = l2.send(tmp)
        tmp = l1.send(ret)
        

# 使用生产者/消费者模型制造产品
def consumer():
    while True:
        recv = yield
        print('收到了：%d' % recv)

def producter(bk):
    i = 0
    while True:
        if i == bk: break
        yield i
        i += 1
        

def run2():
    recv = consumer()
    next(recv)
    for i in producter(20):
        recv.send(i)
        
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
        
if __name__ == '__main__':
#     run1()
    run2()
    
#     from itertools import islice
#     gen = islice(fib(), 10)
#     for i in gen:
#         print(i)
