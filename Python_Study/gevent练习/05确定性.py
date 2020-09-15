#！/usr/bin/python
#coding:utf-8

'''
    Created on 2016年7月25日
    @author: xiongqiao
    @attention：
'''

# 确定性
# greenlet具有确定性。在相同配置相同输入情况下，它们总是会产生相同的输出。

import time

def echo(i):
    time.sleep(0.001)
    return i

def main():
    # Deterministic Gevent Pool
    from gevent.pool import Pool
    p = Pool(10)
    run1 = [a for a in p.imap_unordered(echo, range(10))]
    run2 = [a for a in p.imap_unordered(echo, range(10))]
    run3 = [a for a in p.imap_unordered(echo, range(10))]
    run4 = [a for a in p.imap_unordered(echo, range(10))]
    print( run1 == run2 == run3 == run4 )
    
    # Non Deterministic Process Pool
    from multiprocessing.pool import Pool
    p = Pool(10)
    run1 = [a for a in p.imap_unordered(echo, range(10))]
    run2 = [a for a in p.imap_unordered(echo, range(10))]
    run3 = [a for a in p.imap_unordered(echo, range(10))]
    run4 = [a for a in p.imap_unordered(echo, range(10))]
    print(run1)
    print(run2)
    print(run3)
    print(run4)

    print( run1 == run2 == run3 == run4 )

if __name__ == '__main__':
    main()
