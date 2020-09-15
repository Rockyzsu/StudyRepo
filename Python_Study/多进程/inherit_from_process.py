# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月3日
    @author: xiongqiao
    @attention：
'''

import multiprocessing


class Worker(multiprocessing.Process):
    def run(self):
        print('In %s' % self.name)



if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    map(lambda x: x.join(), jobs)
    