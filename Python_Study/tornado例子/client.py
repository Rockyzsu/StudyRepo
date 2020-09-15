#!urs/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
# import requests
import tornado.httpclient


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/blocking', BlockHandler),
            ('/non_blocking', NonBlockHandler),
        ]
        super(Application, self).__init__(handlers)


class BlockHandler(tornado.web.RequestHandler):
    # AsyncHttpClient本身的限制（默认情况下只允许同时发起10个client）。详情请参考
    # tornado源码的 simple_httpclient.py文件。
    # ioloop本身的限制(为了保证线程的稳定性，默认只开启了10个线程来支持并发)。详情请
    # 参考tornado源码的 netutil.py文件。
    # 可以通过设定参数来提高并发能力(将 tornado.httpclient.AsyncHTTPClient()改为
    # tornado.httpclient.AsyncHTTPClient(max_clients=100))。
    @tornado.web.asynchronous
    def get2(self, *args, **kwargs):
        client = tornado.httpclient.AsyncHTTPClient(max_clients=100)
        client.fetch('http://localhost:8888/blocking', callback=self.on_response)
        
        # 不采用asynchronous装饰器
#         future = client.fetch('http://localhost:8888/blocking')
#         tornado.ioloop.IOLoop.current().add_future(future, callback=self.on_response)

        # future方法
        # future的add_done_callback方法，是告诉ioloop当future的状态变更为完成的时候，
        # 就调用包裹在add_done_callback中的函数(或匿名函数)
#         future.add_done_callback(lambda x: future.set_result(x.result()))
        
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # Task方法
        '''
        tornado.gen.Task需要配合tornado.gen.coroutine装饰器来完成代码的运行，因为
        Task利用了yield，它的隐藏方法run()利用了gen.send()方法，所以gen模块必须要
                用coroutine装饰器。
                利用coroutine的方式比较明显的一个地方是，代码不用再分开了, 这个是Python语言
                的一个特性，yield关键字可以赋值给一个变量, 因此就不需要callback了。
                这样有什么好处？ 本地变量和全局变量不用传递了，默认就是共享的。
        '''
        client = tornado.httpclient.AsyncHTTPClient()
        content = yield tornado.gen.Task(client.fetch, ('http://localhost:8888/blocking'))
        result = dict(content.headers)
        result.update({'content': content.body})
        self.write(result)
        self.finish()
        
    def on_response(self, content):
        result = dict(content.headers)
        result.update({'content': content.body})
        self.write(result)
        self.finish()


class NonBlockHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('non_blocking')


if __name__ == "__main__":
    tornado.options.define("port", default=8000, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()    