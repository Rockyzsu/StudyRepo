# !/usr/bin/python
#coding:utf-8


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# HTTP状态码
# 404：路径无法匹配任何RequestHandler类相对应的模式
# 400：如果你调用了一个没有默认值的get_argument函数，并且没有发现给定名称的参数。
# 405：请求的时候，tornado未定义指定方法（比如post请求，但是只有get）。
# 500：当程序遇到任何不能让其退出的错误时，返回500。代码中任何没有捕获的异常也会导致500错误。
# 200：成功。


from tornado.options import define, options
# options用来从命令行中读取设置
define("port", default=8000, help="run on the given port", type=int)
# type进行基本参数类型验证，当不合适的类型被给出时抛出一个异常。

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
        
    def write_error(self, status_code, **kwargs):
        # 重写这个方法替代默认的错误相应
        self.write('Gosh darnit, user! You caused a %d error.' % status_code)
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()