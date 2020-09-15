# !/usr/bin/python
#coding:utf-8


import re

# ?()    条件    (?(backreference)true-regex)
# 其中?表明这是一个条件，括号里backreference是一个回溯引用，true-regex是一个只在
# backreference存在时才会被执行的子表达式

# ?()|    条件    (?(backreference)true-regex|false-regex)
# 这个语法接受一个条件和两个将分别在这个条件得到满足和没有得到满足时执行的子表达式

def foo1():
    string = """
    123-456-7890
    (123)456-7890
    (123)-456-7890
    (123-456-7890
    1234567890
    123 456 7890
    """
    #匹配北美号码
    pattern = re.compile(r'((\()?\d{3}(?(1)\)|-)\d{3}-\d{4})')
#     pattern = re.compile(r'((\()?\d{3}\d{3}-\d{4})')
    m = pattern.findall(string)
    if m:
        print(m)
        
def foo2():
    string = '''11111
    22222
    33333-
    44444-4444
    '''
#     p = re.compile(r'(\d{5}(?(?=-)-\d{4}))')
    p = re.compile(r'(\d{5}(-\d{4})?)')
    m = p.findall(string)
    if m:
        print(m)


def main():
    foo1()
    foo2()

if __name__ == '__main__':
    main()
