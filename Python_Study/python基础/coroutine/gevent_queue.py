
from time import sleep
import requests
import gevent
from gevent.queue import Queue
from gevent.pool import Pool
from gevent import monkey
monkey.patch_socket()

# put和get都有非阻塞的版本，put_nowait和get_nowait不会阻塞，然而在操作不能完成时抛出
# gevent.queue.Empty或gevent.queue.Empty异常。

pool = Pool()
tasks = Queue()
nums = 0

def worker():
    global nums
    while nums:
        task = tasks.get()
        print(nums)
        nums -= 1
    print('Quitting time!')


def boss():
    # headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    def _(url):
        # response = requests.get(url, headers=headers)
        response = requests.get(url)
        # sleep(300 / 1000)
        print(url)
        tasks.put_nowait(url)

    global nums
    page_url_base = 'http://www.mala.cn/forum-70-{0}.html'
    page_urls = [page_url_base.format(i) for i in range(1, 100)]
    nums = len(page_urls)
    # [pool.apply_async(_, args=(obj,)) for obj in page_urls]
    [pool.apply(_, args=(obj,)) for obj in page_urls]
    # pool.map_async(_, page_urls)


import time
st = time.time()
gevent.spawn(boss).join()
gevent.spawn(worker).join()
print('total: ', time.time() - st)
