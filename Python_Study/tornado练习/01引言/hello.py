# !/usr/bin/python
#coding:utf-8


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
# options用来从命令行中读取设置
define("port", default=8000, help="run on the given port", type=int)
# type进行基本参数类型验证，当不合适的类型被给出时抛出一个异常。

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.get_argument('msg'))
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()