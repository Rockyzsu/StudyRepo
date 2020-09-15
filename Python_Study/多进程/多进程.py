# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月29日
    @author: xiongqiao
    @attention：
'''


import time
import multiprocessing


def worker(num):
    print('workworkernum')
    
def func01():
    name = multiprocessing.current_process().name
    print(name, 'starting')
    time.sleep(2)
    print(name, 'exiting')
    
def func02():
    name = multiprocessing.current_process().name
    print(name, 'starting')
    time.sleep(3)
    print(name, 'exiting')
    
    
    
if __name__ == '__main__':
#     for i in range(5):
#         p = multiprocessing.Process(target = workworkergs = (i, ))
#         p.start()
    f01 = multiprocessing.Process(name = 'func01', target = func01)
    f02 = multiprocessing.Process(name = 'func02', target = func02)
    default = multiprocessing.Process(target = func01)
    f01.start()
    f02.start()
    default.start()