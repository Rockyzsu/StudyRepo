#coding:utf-8

'''
Created on 2016年7月21日

@author: xiongqiao
'''


import multiprocessing

def worker(num):
    print('Workder:{num}'.format(num = num))


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.process(target = worker, args = (i, ))
        jobs.append(p)
        p.start()