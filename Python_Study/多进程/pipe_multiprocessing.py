# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''


import multiprocessing

def proc1(pipe):
    pipe.send('hello')
    print('proc1 rec:', pipe.recv())
    
def proc2(pipe):
    print('proc2 rec:', pipe.recv())
    pipe.send('hello, too')


if __name__ == '__main__':
    #build a pipe
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target = proc1, args = (pipe[0], ))
    p2 = multiprocessing.Process(target = proc2, args = (pipe[1], ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
