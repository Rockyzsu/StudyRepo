# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午7:14
# @File    : fileinput_test.py

import fileinput

with fileinput.input(files=('test.txt',)) as f:
    for line in f:
        print(line, end='')
