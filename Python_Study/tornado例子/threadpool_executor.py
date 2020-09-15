#!urs/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.gen                      
import requests
import tornado.concurrent                # 导入 tornado.concurrent 并发模块


'''
自从了coroutine、threadpool、processpool之后，tornado算是一个里程碑式的解放了对异步
的要求， 原因是tornado的异步库只针对httpclient, 没有针对mysql或者其他数据库的异步库
(自己写一个异步库难度太高，因为辗转十几个源码文件的重度调用以及每个类中的状态控制)。
coroutine结合threadpool让编写异步代码不再拆成多个函数，变量能够共享，堵塞的代码
（例如 requests、mysql.connect、密集计算）可以不影响ioloop，形成真正的闭合。
'''


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/blocking', BlockHandler),
            ('/non_blocking', NonBlockHandler),
        ]
        super(Application, self).__init__(handlers)
        # 建议设定为CPU核心数量 * 4或8或16也是可以接受的, 取决于计算量，计算量越大设定的值应该越小.
        self.executor = tornado.concurrent.futures.ThreadPoolExecutor(16)


class BlockHandler(tornado.web.RequestHandler):
    @property
    def executor(self):
        return self.application.executor

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        print(dir(self))
        content = yield self.executor.submit(requests.get, ('http://localhost:8888/blocking'))
        result = dict(content.headers)
        result.update({'content': content.content})
        self.write(result)


class NonBlockHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('non_blocking')


if __name__ == "__main__":
    # 通过define 可以为options增加变量.
    tornado.options.define("port", default=80, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()    