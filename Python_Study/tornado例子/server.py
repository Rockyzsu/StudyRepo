#!urs/bin/env python
#coding:utf-8

import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.options
import tornado.httpserver


class BlockingHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # 如果这条命令没看懂的话，请参考这个链接: http://www.tornadoweb.org/en/stable/faq.html
        yield tornado.gen.sleep(1)

        # 另一个sleep
#         io_loop = tornado.ioloop.IOLoop.current()
#         yield tornado.gen.Task(io_loop.add_timeout, io_loop.time() + 1)
        self.write('ok')
     
# from tornado import concurrent   
# import time
# executor = concurrent.futures.ThreadPoolExecutor(8)
# 
# class ThreadPoolHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         yield executor.submit(time.sleep, 1)
#         self.write('ok')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/blocking', BlockingHandler),
#             ('/blocking2', ThreadPoolHandler),
        ]
        super(Application, self).__init__(handlers)


if __name__ == "__main__":
    tornado.options.define("port", default=8888, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()    