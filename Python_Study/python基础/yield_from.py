#!urs/bin/env python
#coding:utf-8

# yield from

'''
Python3.3版本的PEP 380中添加了yield from语法，允许一个generator生成器将其部分操作委
派给另一个生成器。其产生的主要动力在于使生成器能够很容易分为多个拥有send和throw方法的
子生成器，像一个大函数可以分为多个子函数一样简单。Python的生成器是协程coroutine的一种
形式，但它的局限性在于只能向它的直接调用者yield值。这意味着那些包含yield的代码不能像
其他代码那样被分离出来放到一个单独的函数中。这也正是yield from要解决的。
虽然yield from主要设计用来向子生成器委派操作任务，但yield from可以向任意的迭代器委派
操作；对于简单的迭代器，yield from iterable本质上等于for item in iterable: yield item
的缩写版，如下所示：
>>> def g(x):
...     yield from range(x, 0, -1)
...     yield from range(x)
...
>>> list(g(5))
[5, 4, 3, 2, 1, 0, 1, 2, 3, 4]

然而，不同于普通的循环，yield from允许子生成器直接从调用者接收其发送的信息或者抛出调
用时遇到的异常，并且返回给委派生产器一个值，如下所示：
'''
def accumulate():               # 子生成器，将传进的非None值累加，传进的值若为None，则返回累加结果
    tally = 0
    while 1:
        n = yield
        if n is None:
            return tally
        tally += n

def gather_tallies(tallies):    # 外部生成器，将累加操作任务委托给子生成器
    while 1:
        tally = yield from accumulate()
        tallies.append(tally)

def foo():
    tallies = []
    acc = gather_tallies(tallies)
    next(acc)           # 使累加生成器准备好接收传入值
    for i in range(4):
        acc.send(i)
    acc.send(None)      # 结束第一次累加
    
    for i in range(5):
        acc.send(i)
    acc.send(None)      # 结束第二次累加
    
    print(tallies)      # 输出最终结果
    
'''
总结如下：
1. 迭代器（即可指子生成器）产生的值直接返还给调用者。
2. 任何使用send()方法发给委派生产器（即外部生产器）的值被直接传递给迭代器。如果send值
是None，则调用迭代器next()方法；如果不为None，则调用迭代器的send()方法。如果对迭代器
的调用产生StopIteration异常，委派生产器恢复继续执行yield from后面的语句；若迭代器产
生其他任何异常，则都传递给委派生产器。
3. 除了GeneratorExit 异常外的其他抛给委派生产器的异常，将会被传递到迭代器的throw()方
法。如果迭代器throw()调用产生了StopIteration异常，委派生产器恢复并继续执行，其他异常
则传递给委派生产器。
4. 如果GeneratorExit异常被抛给委派生产器，或者委派生产器的close()方法被调用，如果迭
代器有close()的话也将被调用。如果close()调用产生异常，异常将传递给委派生产器。否则，
委派生产器将抛出GeneratorExit异常。
5. 当迭代器结束并抛出异常时，yield from表达式的值是其StopIteration 异常中的第一个参数。
6. 一个生成器中的return expr语句将会从生成器退出并抛出 StopIteration(expr)异常。
'''
    
# yield from作用
'''
将yield from视为提供了一个调用者和子生成器之间的透明的双向通道。包括从子生成器获取
数据以及向子生成器传送数据。
'''
# 1. 利用yield from从生成器读取数据
def reader():
    # 模拟从文件读取数据的生成器
    for i in range(4):
        yield '<< %s' % i

def reader_wrapper(g):
    # 循环迭代从reader产生的数据 
    for v in g:
        yield v
    # 我们可以用yield from语句替代reader_wrapper(g)函数中的循环
#     yield from g

def foo2():
    wrap = reader_wrapper(reader())
    for i in wrap:
        print(i)

# 2.利用yield from语句向生成器（协程）传送数据
# 首先创建一个生成器writer，接收传送给它的数据，并写进套接字，文件等；

def writer():
    # 读取send传进的数据，并模拟写进套接字或文件
    while True:
        w = yield    # w接收send传进的数据
        print('>> ', w)

# 现在的问题是，包装器函数如何传送数据给writer函数，使得传递给包装器的数据都能够显式
# 地传递给writer函数？！
# 即我们期待得到如下结果：
def writer_wrapper(coro): return coro

# 很显然，包装区需要接收数据并显式传递给生成器，并且需要处理for循环耗尽是生成器产生的
# StopIteration异常，显然包装器只用for循环已经不能满足需求，满足情况的一般版本如下： 
def writer_wrapper2(coro):
    coro.send(None)                 # 生成器准备好接收数据
    while True:
        try:
            x = (yield)             # x接收send传进的数据
            coro.send(x)            # 然后将x在send给writer子生成器
        except StopIteration:       # 处理子生成器返回的异常
            pass

# 包装器也是个生成器，上面所有复杂的写法也可以用yield from替换：

def writer_wrapper3(coro):
    yield from coro

def foo3():
    w = writer()
#     wrap = writer_wrapper(w)
#     wrap.send(None)  # 生成器准备好接收数据，也可以next(wrap)
#     for i in range(4):
#         wrap.send(i)
        
#     w = writer_wrapper2(w)
#     next(w)
#     for i in range(4):
#         w.send(i)
        
    w = writer_wrapper3(w)
    w.send(None)
    for i in range(4):
        w.send(i)

# 3. 利用yield from向生成器传送数据–处理异常
# 更进一步，如果我们的子生成器即writer需要处理异常该怎么办？假设writer需要处理
# SpamException异常，遇到这个异常打印***，代码如下：
class SpamException(Exception):
    pass

def writer2():
    while True:
        try:
            w = (yield)
        except SpamException:
            print('***')
        else:
            print('>> ', w)

# 如果使用上一个一般版本的包装器writer_wrapper(coro1)，会有什么结果？试验如下： 
def foo4():
    w = writer2()
    wrap = writer_wrapper(w)
#     wrap = writer_wrapper4(w) # 效果一样
#     wrap = writer_wrapper5(w) # 效果一样
    wrap.send(None)  # "prime" the coroutine
    for i in [0, 1, 2, 'spam', 4]:
        if i == 'spam':
            wrap.throw(SpamException)
        else:
            wrap.send(i)

# 可以看出，这行不通，因为x = (yield)语句仅能够引发异常，然后停止运行。我们可以手工在
# 包装器writer_wrapper(coro1)中添加异常处理，并传递或者抛出异常给子生成器writer。
# （实际上x = (yield)已经可以throw出异常了，可能是版本修改了。
def writer_wrapper4(coro1):
    # 手工处理异常被抛给子生成器
    coro1.send(None)    # 生成器准备好接收数据
    while True:
        try:
            try:
                x = (yield)
            except Exception as e:   # 捕获异常
                coro1.throw(e)
            else:
                coro1.send(x)
        except StopIteration:
            pass

# 同样的，这一堆复杂的代码，也可以用yield from语句替换，并且功能完全一样！！！
def writer_wrapper5(coro):
    yield from coro

# 当然yield from不仅有这两个处理情况，还有之前我们提到的：外部生成器关闭，子生成器也
# 会关闭；子生成器返回一个值得情况（上文第二个代码例子），等等。 

if __name__ == '__main__':
#     foo()
#     foo2()
#     foo3()
    foo4()