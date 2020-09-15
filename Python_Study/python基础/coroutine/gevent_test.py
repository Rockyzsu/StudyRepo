
import time
from gevent import pool, queue, sleep, monkey
monkey.patch_socket()
Q = queue.Queue()
p = pool.Pool()
r = []


def bar(num):
    r.append(num + 1)
    Q.put(num + 1)


if __name__ == '__main__':
    l = [23, 9, -23, 9, 0, 12]
    [p.apply_async(bar, args=(i,)) for i in l]

    while True:
        try:
            data = Q.get(timeout=2000)
            print(data)
        except:
            pass