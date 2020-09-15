

from gevent import sleep
from gevent.pool import Pool
from gevent.queue import Queue
from gevent import monkey
monkey.patch_socket()
pool = Pool(20)
qu = Queue()



class PageBase(object):
    def __init__(self):
        self.delay = 30


class CreateTree(PageBase):
    # 创建tree
    name = "创建树"

    def process(self, stream):
        '''异步生成文档树
        :param stream:stream是一个生成器，每一个元素为实际的url
        :return:tree对象及其url/参数
        :bug:这个方法未能完全达到要求，启动时有阻塞，以及不稳定。
        '''
        def _(obj):
            attribute = 'url' if isinstance(obj, str) else 'params'
            setattr(crawler, attribute, obj)
            t = crawler.crawl()
            if t:
                qu.put((t, obj))
            sleep(self.delay / 1000)

        crawler = GetHTML()
        crawler.init()
        copy_attribute(crawler, self)
        objects = []
        while True:
            try:
                u = next(stream)
                objects.append(u)
            except StopIteration:
                break
        # 建立池和队列
        [pool.apply_async(_, args=(obj, )) for obj in objects]
        pool.join()

        time.sleep(1)
        while True:
            try:
                tree, obj = qu.get(timeout=1)
                if tree:
                    yield tree, obj
            except Empty:
                break