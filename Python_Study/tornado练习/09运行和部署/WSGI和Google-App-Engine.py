#!urs/bin/env python
#coding:utf-8



'''
Tornado通常是独立运行的, 不需要一个WSGI容器. 然而, 在一些环境中 (例如Google App 
Engine), 只运行WSGI, 应用程序不能独立运行自己的 服务. 在这种情况下, Tornado支持一个
有限制的操作模式, 不支持异步 操作但允许一个Tornado功能的子集在仅WSGI环境中. 以下功
能在WSGI 模式下是不支持的, 包括协程, @asynchronous 装饰器, AsyncHTTPClient, auth 
模块和WebSockets.
你可以使用 tornado.wsgi.WSGIAdapter 把一个Tornado Application 转换成WSGI应用. 在这
个例子中, 配置你的WSGI容器发 现 application 对象:
import tornado.web
import tornado.wsgi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

tornado_app = tornado.web.Application([
    (r"/", MainHandler),
])
application = tornado.wsgi.WSGIAdapter(tornado_app)

查看 appengine example application 以 了解AppEngine在Tornado上开发的完整功能.
'''