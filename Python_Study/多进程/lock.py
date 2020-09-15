# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''

from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    print('hello world', i)
    l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        a = Process(target=f, args=(lock, num))
        a.start()
        a.join()
