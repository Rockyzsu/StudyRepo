# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''


import os
import multiprocessing
import time

def inputQ(queue):
    info = str(os.getpid()) + '(put)'
    queue.put(info)
    
def outputQ(queue, lock):
    info = queue.get()
    lock.acquire()
    print(str(os.getpid()) + '(get):' + info)
    lock.release()
   

if __name__ == '__main__':
    record1 = []
    record2 = []
    lock = multiprocessing.Lock()
    queue = multiprocessing.Queue(3)
    
    for i in range(10):
        process = multiprocessing.Process(target = inputQ, args = (queue, ))
        process.start()
        record1.append(process)
        
    for i in range(10):
        process = multiprocessing.Process(target = outputQ, args = (queue, lock))
        process.start()
        record2.append(process)
        
    map(lambda x: x.join(), record1)
    queue.close()   #No more object will come, close the queue
    map(lambda x: x.join(), record2)
