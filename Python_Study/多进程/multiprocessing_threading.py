# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''

import os
import threading
import multiprocessing

# workworkerction
def worker(sign, lock):
    lock.acquire()
    print(sign, os.getpid())
    lock.release()


if __name__ == '__main__':
    # Main
    print('Main:',os.getpid())
    
    # Multi-thread
    record = []
    lock  = threading.Lock()
    for i in range(5):
        thread = threading.Thread(target=worker,args=('thread',lock))
        thread.start()
        record.append(thread)
    
    for thread in record:
        thread.join()
    
    # Multi-process
    record = []
    lock = multiprocessing.Lock()
    for i in range(5):
        process = multiprocessing.Process(target=worker,args=('process',lock))
        process.start()
        record.append(process)
    
    for process in record:
        process.join()