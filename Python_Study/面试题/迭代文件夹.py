#!usr/bin/env python
#coding:utf-8


import os

def print_directory_contents(dir_):
    for root, ds, files in os.walk(dir_):
        print(root)
        for o in [os.path.join(root, d) for d in ds]:
            print(o)
        for o in [os.path.join(root, file) for file in files]:
            print(o)

if __name__ == '__main__':
    print_directory_contents('E:/文档/C')