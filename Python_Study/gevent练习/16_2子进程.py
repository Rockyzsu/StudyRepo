#!urs/bin/env python
#coding:utf-8

# 很多人也想将gevent和multiprocessing一起使用。最明显的挑战就是multiprocessing提供
# 的进程间通信默认不是协作式的。由于基于multiprocessing.Connection的对象（例如Pipe）
# 暴露了它们下面的文件描述符，gevent.socket_read和wait_write可以用来直接读写之前
# 协作式的等待ready-to-read/ready-to-write事件。



import gevent
from multiprocessing import Process, Pipe
from gevent.socket import wait_read, wait_write

# To Process
a, b = Pipe()

# From Process
c, d = Pipe()

def relay():
    for i in range(10):
        msg = b.recv()
        c.send(msg + " in " + str(i))

def put_msg():
    for _ in range(10):
        wait_write(a.fileno())
        a.send('hi')
        
def get_msg():
    for _ in range(10):
        wait_read(d.fileno())
        print(d.recv())
        
if __name__ == '__main__':
    proc = Process(target=relay)
    proc.start()
    
    g1 = gevent.spawn(get_msg)
    g2 = gevent.spawn(put_msg)
    gevent.joinall([g1, g2], timeout=1) 
        
# 组合multiprocessing和gevent必定带来依赖操作系统的缺陷，其中有：
# 1. 在兼容POSIX的系统创建子进程之后，在子进程的gevent的状态是不适定的。一个副作用就是，
# multiprocessing.Process创建之前的greenlet创建动作，会在父进程和子进程两方都运行。
# 2. 上面的put_msg()中的a.send()可能依然非协作地阻塞调用的线程：一个ready-to-write
# 事件只保证写了一个byte。在尝试写完成之前底下的buffer可能是满的。
# 3. 上面表示的基于wait_write()/wait_read()的方法在Windows上不工作，因为Windows不能
# 监视pipe事件。
# 解决方案：python的gipc以大体上透明的方式在兼容POSIX和Windows上克服了这些挑战。它
# 提供了gevent感知的基于multiprocessing.Process的子进程和gevent基于pipe的协作式进程
# 间通信。

