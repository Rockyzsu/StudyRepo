# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''

import multiprocessing
import time

def daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    time.sleep(2)
    print('Exiting :', name)

def non_daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    print('Exiting :', name)

if __name__ == '__main__':
    d = multiprocessing.Process(name = 'daemon',target = daemon)
    d.daemon = True

    n = multiprocessing.Process(name = 'non-daemon',target = non_daemon)
    n.daemon = False

    d.start()
    n.start()

    d.join(1)
    print('d.is_alive()', d.is_alive())
    n.join()
