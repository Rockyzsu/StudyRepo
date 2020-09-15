# !/usr/bin/python
#coding:utf-8

import urllib.parse

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument('keyword')
        client = tornado.httpclient.HTTPClient()
        params = {'keyword': keyword}
        response = client.fetch("http://cn.bing.com/search?" + \
                urllib.parse.urlencode(params))
        self.write(response.body.decode())
        

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()