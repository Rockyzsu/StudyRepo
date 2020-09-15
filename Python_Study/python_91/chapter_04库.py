#!usr/bin/env python
#coding:utf-8


# 建议36：掌握字符串的基本用法
# 略


# 建议37：按需选择sort()或者sorted()
'''
1. 相比sort()，sorted()使用的范围更广，两者的函数形式分别如下：
sorted(iterable cmp[, key][, reverse])
s.sorted(iterable cmp[, key][, reverse])
不过在python3中取消掉了cmp参数。取而代之的是functools下面的cmp_to_key()函数。
A. cmp为用户定义的任何比较函数，函数的参数为两个可比较的元素（来自iterable或者list），
函数根据第一个参数与第二个参数的关系依次返回-1、0或者+1（第一个参数小于第二个参数则
返回负数）。默认为None。
B. key是一个带参数的函数，用来为每个元素提取比较值，默认为None（即直接比较每个元素）。
C. reverse表示排序结果是否反转。

2. sort()会修改原来的列表，而sorted()重新生成一个列表。sort()函数不需要复制原有列表，
消耗的内存较少，效率也较高。

3. 无论是sort()还是sorted()函数，传入参数key比传入参数cmp的效率要高。cmp传入的函数在
整个排序过程中会调用多次，函数开销较大；而key针对每个元素仅作一次处理。

4. sorted()函数的功能十分强大，使用它可以方便地针对不同的数据结构进行排序。

itemgetter的源码如下：
class itemgetter:
    """
    Return a callable object that fetches the given item(s) from its operand.
    After f = itemgetter(2), the call f(r) returns r[2].
    After g = itemgetter(2, 5, 3), the call g(r) returns (r[2], r[5], r[3])
    """
    def __init__(self, item, *items):
        if not items:
            def func(obj):
                return obj[item]
            self._call = func
        else:
            items = (item,) + items
            def func(obj):
                return tuple(obj[i] for i in items)
            self._call = func

    def __call__(self, obj):
        return self._call(obj)
'''

def func_37():
    persons = [{'name': 'Jon', 'age': 32}, 
               {'name': 'Alan', 'age': 50}, 
               {'name': 'Bob', 'age': 23}
               ]
    persons.sort(key=lambda x: (x['name'], -x['age']))
    print(persons)
    
    from operator import itemgetter
    # sorted
    # 字典排序
    phonebook = {'Linda': '7750', 'Bob': '9345', 'Carol': '5834'}
    print(sorted(phonebook.items(), key=itemgetter(1)))
    # 多维list排序
    g = [['Bob', 95, 'A'], ['Alan', 86, 'C'], ['Mandy', 82, 'A'], ['Rob', 86, 'E']]
    print(sorted(g, key=itemgetter(2, 1)))
    # 字典中混合list排序
    # 如果字典中的key或者值为列表，需要对列表中的某一个位置的元素排序也是可以做到的。
    d = {'Li': ['M', 7], 'Zhang': ['E', 2], 'Wang': ['P', 3], 'Du': ['C', 2],
         'Ma': ['C', 9], 'Zhe': ['H', 7]
         }
    print(sorted(d.items(), key=lambda k: itemgetter(1)(k[1])))
    # list中混合字典排序
    # 列表中的每一个元素为字典形式，可以针对字典的多个key值进行排序也可。
    g2 = [{'name': 'Bob', 'wins': 10, 'losses': 3, 'rating': 75.00},
          {'name': 'David', 'wins': 3, 'losses': 5, 'rating': 57.00},
          {'name': 'Carol', 'wins': 4, 'losses': 5, 'rating': 57.00},
          {'name': 'Patty', 'wins': 9, 'losses': 3, 'rating': 71.48},
          ]
    print(sorted(g2, key=itemgetter('rating', 'name')))
    
    
# 建议38：使用copy模块深拷贝对象
'''
1. 浅拷贝：构造一个新的复合对象并将原对象中发现的引用插入该对象中，浅拷贝的实现方式有
多种，如工厂函数、切片操作、copy模块中的copy操作等。
2. 深拷贝：也构造一个新的复合对象，但是遇到引用会继续递归拷贝其所指向的具体内容，也就是
说它会针对引用所指向的对象继续执行拷贝，因此产生的对象不受其他引用对象操作的影响。
'''
def func_38():
    # 浅拷贝
    a = ['hello', [123, 234]]
    b = a[:]    # b=a仅仅是多一个引用，在b中的修改都会影响到a
    print([id(x) for x in (a, b)])
    print([id(x) for x in a])
    print([id(x) for x in b])
    # a和b的地址是不同的，但是发现a，b里面的元素地址还是相同的，修改a或者b的list元素
    # 就会导致两个都修改，因为list是可变的，它们共享一个。浅拷贝仅仅是复制了容器中元素
    # 的地址。
    
    # 深拷贝
    print('====================')
    from copy import deepcopy
    a = ['hello', [123, 234]]
    b = deepcopy(a)
    print([id(x) for x in (a, b)])
    print([id(x) for x in a])
    print([id(x) for x in b])   # 'hello'是不可变对象，这个时候它们还是共用它
    a[0] = 'world'
    b[1].append(10)
    print(a)
    print(b)
    
    '''
    1. 赋值是将一个对象的地址赋值给一个变量，让变量指向该地址（ 旧瓶装旧酒 ）。
    2. 浅拷贝是在另一块地址中创建一个新的变量或容器，但是容器内的元素的地址均是源对象
        的元素的地址的拷贝。也就是说新的容器中指向了旧的元素（ 新瓶装旧酒 ）。
    3. 深拷贝是在另一块地址中创建一个新的变量或容器，同时容器内的元素的地址也是新开
        辟的，仅仅是值相同而已，是完全的副本。也就是说（ 新瓶装新酒 ）。
    '''
    

# 建议39：使用Counter进行计数统计
'''
Counter类属于字典类的子类，是一个容器对象，主要用来统计散列对象，支持集合操作+、-、&
和|，其中&和|操作分别返回两个Counter对象各个元素的最小值和最大值，它提供了三种不同的
方式来初始化：
Counter('success')    # 可迭代对象
Counter(s=3, c=2, e=1, u=1)    # 关键字参数
Counter({'s': 3, 'c': 2, 'e': 1, 'u': 1})    # 字典
'''
from collections import Counter
def func_39():
    some_data = ['a', '2', 2, 4, 5, '2', 'b', 4, 7, 'a', 5, 'd', 'a', 'z']
    c = Counter(some_data)
    # elements()获取Counter中的key值
    print(c.elements())
    # most_common()找出前n个出现频率最高的元素以及它们对应的次数
    print(c.most_common(2))
    # 访问不存在元素时，默认返回0,而不是抛出KeyError
    print(c['y'])
    # update()用于被统计对象元素的更新，原有Counter计数器对象与新增元素的统计计数值
    # 相加而不是直接替换它们
    # subtract()方法用于实现计数器对象中元素统计值相减，输入和输出的统计值允许为0或负值。
    c = Counter('success')
    print(c)
    c.update('successfully')
    print(c)
    c.subtract('successfully')
    print(c)
    
    
# 建议40：深入掌握ConfigParser
# 配置文件


# 建议41：使用argparse处理命令行参数
# 标准库还有getopt、optparse，argparse也是。


# 建议42：使用pandas处理大型csv文件
# pandas是一个很强悍的计算模块。


# 建议43：一般情况使用ElementTree解析XML
# xml.dom.minidom和xml.sax是python中处理xml文件很出名的模块，但是它们很不相同。
'''
DOM需要将整个XML文件加载到内存中并解析为一棵树，虽然使用简单，但是占用内存较多，性能
方面不占优势。SAX是基于事件驱动的，虽不需要全部装入XML文件，但其处理过程却较为复杂。
cElementTree是C版本实现，优先选择。
优点：内存上消耗明显低于DOM解析。由于它的底层进行了一定的优化，并且它的iterparse解析
工具支持SAX事件驱动，能够以迭代的形式返回XML部分数据结构，从而避免将整个XML文件加载
到内存中。同时，它也支持XPath查询，非常方便。
在处理XML文件大小在GB或近似GB级别的时候，三方的lxml是个更好的选择。
'''
# from xml.etree import cElementTree


# 建议44：理解pickle优劣
# 它也有C版本实现，优先选择
# import cPickle    


# 建议45：序列化的另一个不错的选择——JSON
# 略。


# 建议46：使用traceback获取栈信息
# 略。


# 建议47：使用logging记录日志信息
# 略。


# 建议48：使用threading模块编写多线程程序
# 略。


# 建议49：使用Queue使多线程编程更安全
# 略。




if __name__ == '__main__':
#     func_37()
#     func_38()
    func_39()
    