# !/usr/bin/python
#coding:utf-8


import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines,
                choice=random.choice)
    
    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit, user! You caused a %d error." % status_code)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates2"),
        
        # static_path指定了应用程序放置静态资源（图像、CSS文件、JS文件等）的目录。
        # tornado模板提供了一个叫做static_url的函数来生成static目录下文件的URL。
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        
        # 在poem.html中static_url的调用示例：
        # <link rel="stylesheet" href="{{ static_url('style.css') }}">
        # 这个对static_url的调用生成了URL的值，并渲染输出类似下面的代码：
        # <link rel="stylesheet" href="/static/style.css?v=ab12">
        # static_url函数创建了一个基于文件内容的hash值，并将其添加到URL末尾（查询字
        # 符串的参数v）。这个hash值确保浏览器总是加载一个文件的最新版而不是之前的缓存
        # 版本。另外一个好处是可以改变应用URL的结构，而不需要改变模板中的代码。
        
        # debug参数调用了一个便利的测试模式：tornado.autoreload模块。此时，一旦主要
        # 的python文件被修改，tornado将会尝试重启服务器，并且在模板改变时会进行刷新。
        # 对于快速改变和实时更新很好，但不要在生产上使用它，因为它将防止tornado缓存
        # 模板！
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()
    
    