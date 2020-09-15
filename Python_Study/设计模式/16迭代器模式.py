#!urs/bin/env python
#coding:utf-8


# 迭代器模式：提供一种方法顺序访问一个聚合对象中各个元素，而又不暴露该对象的内部表示。[DP]
# 当需要访问一个聚集对象，而且不管这些对象时什么都需要遍历的时候，我们就应该考虑使用
# 迭代器模式。
# 现在的高级编程语言很多本身已经把这个模式做在语言中了。



class Iterator(object):
    def __init__(self):
        self._count = 0
        self.idx = -1
        self.items = []
    
    def __getitem__(self, idx):
        return self.items[idx]
    
    def __setitem__(self, idx, v):
        # 用户可以自由设置索引对应的值，如设置0、1、4、7索引及其对应的值，那么2、3、
        # 5、6位置的值自动设置为0。
        try:
            self.items[idx] = v
        except IndexError:
            for i in range(len(self.items), idx):  # 如果报错
                try:
                    self.items[i]
                except IndexError:
                    self.items.append(0)
            self.items.append(v)
            
    def __iter__(self):
        return self
    
    def __next__(self):
        self.idx += 1
        try:
            v = self.items[self.idx]
        except IndexError:
            self.idx = -1
            raise StopIteration     # 迭代完后，抛出这个异常并将索引置回
        return v
    

def run():
    a = Iterator()
    a[0], a[1], a[7], a[3], a[4], a[5] = ('大鸟', '小菜', '行李', 
                                          '老外', '公交内部员工', 
                                          '小偷')
    for i in a:
        if i:
            print('{0} 请购买车票！'.format(i))
    
        
if __name__ == '__main__':
    run()
    
    
    