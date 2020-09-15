#!usr/bin/env python
#coding:utf-8


import os
import sys

def delete(root_dir, arg):
    '''
    @param root_dir:要执行的目录
    @param arg:要删除以什么结尾的文件 
    '''
    if not root_dir:
        print('请输入目录！')
        return
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.split('.')[-1] == arg:
                file = os.path.join(root, file)
                os.remove(file)
                print('删除：%s' % file)


if __name__ == '__main__':
#     delete(sys.argv[1:2][0], sys.argv[2:][0])
    delete('C:\\Users\\Administrator\\Desktop\\肖川', 'pyc')