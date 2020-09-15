#!usr/bin/env python
#coding:utf-8

import re

def find_ip():
    # 分组
    s = '''
    Pingping hong.forta.com [12.159.46.200]
    with 32 bytes of data:
    '''
    p = re.compile(r'(((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}'\
                   '(\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5])')
    m = p.search(s)
    if m:
        print(m.group())
        
def find_email():
    s = '''
    xiongqiao.get@outlook.com
    bb@cc.cn
    '''
#     p = re.compile(r'\w+[\w\.]*@[\w.]+\.\w+')
    p = re.compile(r'((\w+\.)*\w+@(\w+\.)+\w+)')
    m = p.findall(s)
    print(m)

if __name__ == '__main__':
    find_ip()
    find_email()