#!urs/bin/env python
#coding:utf-8

import functools
from functools import *

# 1. partial(func, *args, **keywords) 
def partial(func, *args, **keywords):
    # functools.partial()的大概实现
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

def test_partial():
    basetwo = partial(int, base=2)
    basetwo.__doc__ = 'Convert base 2 string to an int.'
    print(basetwo('10010'))


# 2. update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 默认partial对象没有__name__和__doc__，这种情况下，对于装饰器函数非常难以debug。使用
# update_wrapper()，从原始对象拷贝或加入现有partial对象。
# 它可以把被封装函数的__name__、module、__doc__和__dict__都复制到封装函数去（模块级别
# 常量WRAPPER_ASSIGNMENTS、WRAPPER_UPDATES）
# 这个函数主要用在装饰器函数中，装饰器返回函数反射得到的是包装函数的函数定义而不是原始函数定义。
def wrap(func):
    def call_it(*args, **kwargs):
        """wrap func: call_it"""
        print('before call')
        return func(*args, **kwargs)
    return call_it

@wrap
def hello():
    """say hello"""
    print('hello world')

def wrap2(func):
    def call_it(*args, **kwargs):
        """wrap func: call_it2"""
        print('before call')
        return func(*args, **kwargs)
    return update_wrapper(call_it, func)    # call_it为包装者，func为被包装者

@wrap2
def hello2():
    """test hello"""
    print('hello world2')

def test_update_wraper():
    print(functools.WRAPPER_ASSIGNMENTS)
    print(functools.WRAPPER_UPDATES)
    
    hello()
    print(hello.__name__)
    print(hello.__doc__)

    print
    hello2()
    print(hello2.__name__)
    print(hello2.__doc__)


# 3. wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 它是partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)的简写
def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')

def test_wraps():
    example()
    print(example.__name__)
    print(example.__doc__)
    
    
# 4. reduce(function, iterable[, initializer]) 
# 略。
    
    
# 5. cmp_to_key(func) 
# 将老式的比较函数（comparison function）转化为关键字函数（key function）。与接受
# key function的工具一同使用（如 sorted(), min(), max(), heapq.nlargest(), 
# itertools.groupby())。该函数主要用来将程序转成 Python 3 格式的，因为 Python 3
# 中不支持比较函数。
# 比较函数是可调用的，接受两个参数，比较这两个参数并根据他们的大小关系返回负值、零或正值
# 中的某一个。关键字函数也是可调用的，接受一个参数，同时返回一个可以用作排序关键字的值。
def test_cmp_to_key():
    nums = [-1,-2,3,4,9,2,3,4,5]
    nums.sort(key=cmp_to_key(lambda x, y: y - x))
    print(nums)


# 6. total_ordering 
# 它是针对某个类如果定义了__lt__、 le 、 gt 、__ge__这些方法中的至少一个，使用该装饰器，
# 则会自动的把其他几个比较函数也实现在该类中。 
@total_ordering
class Student(object):
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()
    
    def __lt__(self, other):
        return self.name.lower() < other.name.lower()
    
def test_total_ordering():
    a = Student('dan')
    b = Student('mink')
    print(a > b)


# 7. lru_cache(maxsize=None, typed=False) python3.2 added
# 使用functools模块的lur_cache装饰器，可以缓存最多maxsize个此函数的调用结果，从而提
# 高程序执行的效率，特别适合于耗时的函数。
# maxsize为最多缓存的次数，如果为None，则无限制，设置为2n时，性能最佳；如果typed=True，
# 则不同参数类型的调用将分别缓存，例如f(3)和f(3.0)。
import requests
@lru_cache(maxsize=32)
def get_pep(num):
    'Retrieve text of a Python Enhancement Proposal'
    resource = 'http://www.python.org/dev/peps/pep-%04d/' % num
    proxies = {'http': 'localhost:1080', 'https': 'localhost:1080'}
    try:
        body = requests.get(resource, proxies=proxies)
        return body.content.decode()
    except:
        return 'Not Found'
    
def test_lru_cache():
    for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991:
        pep = get_pep(n)
        print(n, len(pep))
    print(get_pep.cache_info())
    
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def test_lru_cache2():
    print([fib(n) for n in range(16)])
    print(fib.cache_info())


# 8. partialmethod(func, *args, **keywords) python3.4 added
class Cell(object):
    def __init__(self):
        self._alive = False
    @property
    def alive(self):
        return self._alive
    def set_state(self, state):
        self._alive = bool(state)
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)
        
def test_partialmethod():
    c = Cell()
    print(c.alive)
    c.set_alive()
    print(c.alive)


# 9. singledispatch(default) python3.4 added
# 略
    


if __name__ == '__main__':
#     test_partial()
#     test_update_wraper()
#     test_wraps()
    test_cmp_to_key()
#     test_total_ordering()
#     test_lru_cache()
#     test_lru_cache2()
#     test_partialmethod()
    