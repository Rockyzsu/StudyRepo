# !/usr/bin/python
#coding:utf-8


import re

'''
(?=)            正向前查找                向前查找与给定模式相匹配的文本
(?!)            负向前查找                向前查找不与给定模式相匹配的文本
(?<=)            正向后查找              向后查找与给定模式相匹配的文本
(?<!)            负向后查找              向后查找不与给定模式相匹配的文本
'''

string = '''
I paid $30 for 100 apples,
50 oranges, and 60 pears.
I saved $5 on this order.
'''

def foo1():
    #正向后查找
    pattern = re.compile(r'(?<=\$)\d+')
    m = pattern.findall(string)
    if m:
        print(m)
        
def foo2():
    #负向后查找
    pattern = re.compile(r'\b(?<!\$)\d+\b')
    m = pattern.findall(string)
    if m:
        print(m)
        
def foo3():
    #负向后查找，去除\b
    pattern = re.compile(r'(?<!\$)\d+')
    m = pattern.findall(string)
    if m:
        print(m)
        
        
string2 = '''
http://www.google.com/
https://mail.forta.com/
ftp://ftp.forta.com
'''
def foo4():
    #正向前查找
    pattern = re.compile(r'.+(?=:)')
    m = pattern.findall(string2)
    if m:
        print(m)


def main():
    foo1()
    foo2()
    foo3()
    foo4()

if __name__ == '__main__':
    main()
