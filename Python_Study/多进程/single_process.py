# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''


import signal
import time
import multiprocessing


def handler(signum, frame):
    print('single', signum)

def run():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    i = 0
    while i < 10000:
        print('running')
        time.sleep(2)
        i += 1

if __name__ == '__main__':
    p = multiprocessing.Process(target = run)
    p.start()
    #p.join()
    print(p.pid)
    print('master gone')
