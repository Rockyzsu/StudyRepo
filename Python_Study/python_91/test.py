#!usr/bin/env python
#coding:utf-8

# chapter_01引论 引论
import chapter_01

def chapter_01_():
    chapter_01.MAX = 10
#     chapter_01.Min = 20 # 不能通过
    chapter_01.MAX = 30   # 不能通过

def chapter_02():
    import os
    os.system('python -O chapter_02.py')
    
def chapter_06():
    class A(object):
        def __init__(self):
            self.__aa = 10
            
    a = A()
    print(a._A__aa)

if __name__ == '__main__':
#     chapter_01_()
#     chapter_02()
    chapter_06()
