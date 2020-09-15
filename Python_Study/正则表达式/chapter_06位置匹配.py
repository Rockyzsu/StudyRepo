# !/usr/bin/python
#coding:utf-8


import re

def foo1():
    #单词边界
    string = '''The captain wore his cap and proudly as
    he sat listening to the...
    '''
    pattern = re.compile(r'\bcap\b')
    m = pattern.findall(string)
    if m:
        print(m)
        
def foo2():
    #匹配非单词边界
    #匹配字母数字下划线之间，或者非字母数字下划线之间
    string = '''Please enter the nine-digit id as is
    appears on your color - coded pass-key
    '''
    pattern = re.compile(r'\B-\B')
    m = pattern.findall(string)
    if m:
        print(m)
        
        
def foo3():
    #匹配开头
    string = '''wo shi chuan qi
    <?xml version="1.0" encoding=UTF-8 ?>
    asdasbasdf
    hello world.
    '''
    pattern = re.compile(r'^\s*<\?xml.*?\?>')
    m = pattern.search(string)
    if m:
        print(m.group())
        
def foo4():
    #匹配结尾
    string = 'hello kitty, this is good'
#     string = 'hello kitty, this is good 12'
    pattern = re.compile(r'good\s*$')
    m = pattern.search(string)
    if m:
        print(m.group())
        
def foo5():
    #多行模式
    string = '''funasdasd
    // hello
    sgesdf
    // world  
    '''
    pattern = re.compile(r'(?m)^\s*//.*\s*$')
    m = pattern.findall(string)
    if m:
        print(m)
        
def foo6():
    #使用repl替换string中每一个匹配的子串后返回替换后的字符串。
    p = re.compile(r'(\w+) (\w+)')
    s = 'i say, hello world!'
    print(p.sub(r'\2 \1', s))
    
def foo7():
    def func(m):
        return m.group(1).title() + ' ' + m.group(2).title()
    p = re.compile(r'(\w+) (\w+)')
    s = 'i say, hello world!'
    print(p.sub(func, s))


def main():
#     foo1()
#     foo2()
#     foo3()
#     foo4()
    foo5()
    foo6()
    foo7()
    

if __name__ == '__main__':
    main()
