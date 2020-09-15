# !/usr/bin/python
#coding:utf-8


import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')


class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'
    
    
class BookModule(tornado.web.UIModule):
    def render(self, book):
        # render_string方法显式地渲染模板文件，当我们返回给调用者时将其关键字作为一个
        # 字符串。
        return self.render_string('book.html', book=book)
    
    def embedded_javascript(self):
        '''
        当调用模块时，document.write("hi!")将被<script>标签包围，并被插入到<body>的闭
        标签中：
        <script type="text/javascript">
        //<![CDATA[
        document.write("hi!")
        //]]>
        </script>
        '''
        return 'document.write("hi!")'
    
#     def embedded_css(self):
#         '''
#         调用模块时，这条CSS规则被包裹在<style>中，并被直接添加到<head>的闭标签之前：
#         <style type="text/css">
#         .book {background-color:RGB(202,203,208)}
#         </style>
#         '''
#         return ".book {background-color:RGB(202,203,208)}"
    
    def html_body(self):
        # 简单地使用html_body()来闭合</body>标签前添加完整的HTML标记
        return '<script>document.write("Hello!")</script>'

    # 当然添加Javascript和CSS的时候使用本地文件或者网络文件更为靠谱
    def css_files(self):
        return '/static/css/style.css'
    
    def javascript_files(self):
        return 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js'
    
    
class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "recommended.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=[
                {
                    "title":"Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image":"./static/images/book1.jpg",
                    "author": "Toby Segaran",
                    "date_added":1310248056,
                    "date_released": "August 2007",
                    "isbn":"978-0-596-52932-1",
                    "description":"<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                },
            ]
        )
        # 在book.html中有locale.format_date()的使用，它实际调用了tornado.locale模块
        # 提供的日期处理方法。locale.format_date()默认格式化GMT Unix时间戳为：
        # July 9, 2011 at 9:47 pm格式。 
        # relative=False将使其返回一个绝对时间（包含小时和分钟），而
        # full_format=True选项将会展示一个包含月、日、年和时间的完整日期
        # （比如，July 9, 2011 at 9:47 pm），当搭配 shorter=True使用时可以
        # 隐藏时间，只显示月、日和年。

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/hello', HelloHandler), (r'/recommended', RecommendedHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates2'),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        ui_modules={'Book': BookModule, 'Hello': HelloModule}
        # 调用HelloHandler并渲染hello.html时，我们使用了{% module Hello() %}模板
        # 标签来包含HelloModule类中render方法返回的字符串
    )
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()