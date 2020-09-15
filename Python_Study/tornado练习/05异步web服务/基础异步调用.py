# !/usr/bin/python
#coding:utf-8



import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

import urllib.parse

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    # asynchronous会监听gen.coroutine的返回结果(Future)，并在gen.coroutine装饰的
    # 代码段执行完成后自动调用finish。从Tornado 3.1版本开始，只使用@gen.coroutine就可以了。
    @tornado.gen.coroutine
    def get(self):
        keyword = self.get_argument('keyword')
        client = tornado.httpclient.AsyncHTTPClient()
        params = {'q': keyword, 'first': 0}
        response = yield client.fetch("http://cn.bing.com/search?" + urllib.parse.urlencode(params))
        self.write(response.body)
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()
    