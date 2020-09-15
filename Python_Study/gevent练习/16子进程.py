#!urs/bin/env python
#coding:utf-8

# gevent.subprocess，它支持协作式的等待子进程

import gevent
from subprocess import PIPE
from gevent.subprocess import Popen


def cron():
    while True:
        print('cron')
        gevent.sleep(0.2)
        

if __name__ == '__main__':
    g = gevent.spawn(cron)
    sub = Popen(['sleep 1; uname'], stdout=PIPE, shell=True)
    out, err = sub.communicate()
    g.kill()
    print(out.rstrip())