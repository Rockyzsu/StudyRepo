#！/usr/bin/python
#coding:utf-8


import gevent
import signal
def run_forever():
    print('running...')
    gevent.sleep(1000)
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, gevent.shutdown)
    thread = gevent.spawn(run_forever)
    thread.join()
    
