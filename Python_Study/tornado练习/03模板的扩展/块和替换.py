#!urs/bin/env python
#coding:utf-8

'''
为了扩展一个已经存在的模板，我们只需要在新的模板文件的顶部放上一句{% extends 
"filename.html" %}。这样就使新文件继承了filename.html的所有标签，并且覆写为期望的内容。
扩展一个模板使我们复用之前写过的代码更加简单，但是这并不会为我们提供所有的东西，除非
我们可以适应并改变那些之前的模板。所以，block语句出现了。
例（main.html）：
<html>
    <body>
        <header>
            {% block header %} {% end %}
        </header>
        <content>
            {% block body %} {% end %}
        </content>
        <footer>
            {% block footer %} {% end %}
        </footer>
    </body>
</html>
我们扩展这个父模板时（index.html）：
{% extends "main.html"}
<html>
    <body>
        {% block header %}
            <h1>{{ header_text }}</h1>
        {% end %}
        {% block body %}
            <p>Hello from the child template!</p>
        {% end %}
        {% block footer %}
            <p>{{ footer_text }}</p>
        {% end %}
    </body>
</html>
加载模板代码：
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", header_text="Header goes here",
        footer_text="Footer goes here"
        )
        
一个语法错误或者没有闭合的{% block %}语句可以使得浏览器直接显示500: Intermal Server Error。
'''

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define
define("port", default=8000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            header_text = "Header goes here",
            footer_text = "Footer goes here"
        )

if __name__ == '__main__':
    app = tornado.web.Application(
        handlers=[(r'/', MainHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    print('Server is running!')
    tornado.ioloop.IOLoop.instance().start()

        