#!urs/bin/env python
#coding:utf-8

import gevent
import time
import gipc
def main():
    with gipc.pipe() as (r, w):
        p = gipc.start_process(target=child_process, args=(r, ))
        p = gipc.start_process(target=random_process)
        wg = gevent.spawn(writegreenlet, w)
        try:
            p.join()
        except KeyboardInterrupt:
            wg.kill(block=True)
            p.terminate()
        p.join()
        
        
def writegreenlet(writer):
    num = 0
    while True:
        num += 1
        writer.put(num)
        gevent.sleep(1)
        
        
def child_process(reader):
    while True:
        print("Child process got message from pipe:\n\t'%s'" % reader.get())
        
        
def random_process():
    while True:
        time.sleep(1)
        print('random')
        
        
if __name__ == "__main__":
    main()