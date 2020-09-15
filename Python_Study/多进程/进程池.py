# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月29日
    @author: xiongqiao
    @attention：
'''

import multiprocessing
import time

def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    for i in range(4):
        msg = "hello %d" %(i)
        pool.apply(func, (msg, ))

    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。
    #执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print("Sub-process(es) done.")