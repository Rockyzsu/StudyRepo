# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月29日
    @author: xiongqiao
    @attention：
'''


from multiprocessing import Pool, Manager


def write(q, lock):
    for i in range(1000):
        lock.acquire()
        q.put(i)
        print('Write %d into queue.' % i)
        lock.release()
    lock.acquire()
    q.put('END')
    lock.release()

def get(q, lock):
    while True:
        if not q.empty():
            value = q.get(False)
            if 'END' == value:
                break
            print('Get %d from queue.' % value)
            


def main():
    pool = Pool()
    manager = Manager()
    q = manager.Queue(maxsize = 100)  
    lock = manager.Lock()
    pool.apply_async(write, args=(q, lock))    
    pool.apply_async(get, args=(q, lock))
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
