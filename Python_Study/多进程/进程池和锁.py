# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月29日
    @author: xiongqiao
    @attention：
'''

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random

# 写数据进程执行的代码:
def write(q,lock):
    for value in ['A', 'B', 'C']:
        lock.acquire() #加上锁   
        print('Put %s to queue...' % value)     
        q.put(value)        
        lock.release() #释放锁  

# 读数据进程执行的代码:
def read(q):
    while True:
        if not q.empty():
            value = q.get(False)
            print('Get %s from queue.' % value)
            time.sleep(random.random())
        else:
            break

if __name__=='__main__':
    manager = multiprocessing.Manager()
    # 父进程创建Queue，并传给各个子进程：
    q = manager.Queue()
    lock = manager.Lock() #初始化一把锁
    p = Pool()
    pw = p.apply_async(write,args=(q,lock))    
    pr = p.apply_async(read,args=(q,))
    p.close()
    p.join()
    
    print('所有数据都写入并且读完')
