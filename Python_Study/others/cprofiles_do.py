# !/usr/bin/python
#coding:utf-8



import cProfile
import time


def fast():
    time.sleep(0.001)
    
def slow():
    time.sleep(0.01)
    
def very_slow():
    for _ in range(100):
        fast()
        slow()
    time.sleep(0.1)    


def main():
    cProfile.run('very_slow()', 'prof.txt')
    import pstats
    p = pstats.Stats('prof.txt')
    p.sort_stats('time').print_stats()

if __name__ == '__main__':
    main()
