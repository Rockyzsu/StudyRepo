#!urs/bin/env python
#coding:utf-8


import tornado.web
import tornado.httpserver


# 默认情况下current_user是空。
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # 为了在应用中实现用户认证，需要在请求处理函数中覆写这个方法来判断当前用户，
        # 比如可以基于cookie的值。
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
#     def get(self):
#         if not self.current_user:
#             self.redirect("/login")
#             return
#         name = tornado.escape.xhtml_escape(self.current_user)
#         self.write("Hello, " + name)
        
    @tornado.web.authenticated
    def get(self):
        # 可以使用tornado.web.authenticated装饰器要求用户登录。如果方法带有这个装饰器
        # 且用户没有登录，用户将会被重定向到login_url（另一个应用设置）。
        # tornado.web.authenticated装饰器是if not self.current_user: self.redirect()
        # 的简写，可能不适合非基于浏览器的登录方案。
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")



if __name__ == "__main__":
    settings = {
                'cookie_secret': "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                'login_url': '/login'
                }
#     application = tornado.web.Application([(r"/", MainHandler), (r"/login", LoginHandler),],
#                                           cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
#                                           )
    application = tornado.web.Application([(r"/", MainHandler), (r"/login", LoginHandler),], 
                                          **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()