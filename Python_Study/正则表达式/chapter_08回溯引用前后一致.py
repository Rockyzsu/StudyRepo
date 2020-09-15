# !/usr/bin/python
#coding:utf-8


import re

string = '''
<BODY>
<h1>Hello World</h2>
<h2>It's bad</h2>
</BODY>
'''

def foo1():
    pattern = re.compile(r'<[Hh][1-6]>.*?</[Hh][1-6]>')
    m = pattern.findall(string)
    if m:
        print(m)
        
def foo2():
    # 回溯引用指的是模式的后半部分引用在前半部分中定义的子表达式
    # \1代表第一个字表达式，\2代表第二个字表达式，依此类推。
    # 在许多实现里\0用来代表整个正则表达式。
    pattern = re.compile(r'<h([1-6])>.*?</h\1>')
    m = pattern.search(string)
    if m:
        print(m.group())
        
        
def main():
    foo1()
    foo2()    

if __name__ == '__main__':
    main()
