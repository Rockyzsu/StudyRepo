#!urs/bin/env python
#coding:utf-8


import pymongo
import time


def foo():
    # 数据准备
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn["bookstore"]
    db.books.insert({
                     "title":"Programming Collective Intelligence",
                     "subtitle": "Building Smart Web 2.0 Applications",
                     "image":"/static/images/22.gif",
                     "author": "Toby Segaran",
                     "date_added":1310248056,
                     "date_released": "August 2007",
                     "isbn":"978-0-596-52932-1",
                     "description":"<p>[...]</p>"
    })
    db.books.insert({
                     "title":"RESTful Web Services",
                     "subtitle": "Web services for the real world",
                     "image":"/static/images/book1.jpg",
                     "author": "Leonard Richardson, Sam Ruby",
                     "date_added":1311148056,
                     "date_released": "May 2007",
                     "isbn":"978-0-596-52926-0",
                     "description":"<p>[...]</p>"
    })



import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port",default=8000,help="runonthegivenport",type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/recommended", RecommendedHandler),
            # BookEditHandler处理了两个不同路径模式的请求，其中一个是/add，提供不存在
            # 信息的编辑表单，因此可以向数据库添加一本新的数据；
            # 另一个/edit/([\w\-]+)则根据书籍的ISBN渲染一个已存在的书籍表单。
            (r"/edit/([\w\-]+)", BookEditHandler),
            (r"/add", BookEditHandler)
        ]
        settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        ui_modules={"Book": BookModule},
        debug=False,
        )
        conn = pymongo.MongoClient("localhost", 27017)
        self.db = conn["bookstore"]
        tornado.web.Application.__init__(self, handlers,**settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title = "Burt's Books | Home",
            header_text = "Welcome to Burt's Books!",
        )
    
    
class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.books
        books = coll.find()
        self.render(
            "recommended.html",
            page_title = "Burt's Books | Recommended Reading",
            header_text = "Recommended Reading",
            books = books
        )
    
    
class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string(
            "book.html",
            book=book,
        )
        
    def css_files(self):
        return "/static/css/style.css"

    def javascript_files(self):
        return "/static/js/script.js"
    
    
# 编辑和添加书籍
class BookEditHandler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        book = {}
        if isbn:
            coll = self.application.db.books
            db_book = coll.find_one({"isbn": isbn})
            book = db_book if db_book else {}
        self.render("book_edit.html",
            page_title="Burt's Books",
            header_text="Edit book",
            book=book)
        
    def post(self, isbn=None):
        book_fields = ['isbn', 'title', 'subtitle', 'image',
                       'author','date_added', 'date_released', 
                       'description'
                       ]
        coll = self.application.db.books
        book = dict()
        if isbn:
            db_book = coll.find_one({"isbn": isbn})
            book = db_book if db_book else {}
        for key in book_fields:
            book[key] = self.get_argument(key, None)
        if isbn:
            coll.save(book)
        else:
            book['date_added'] = int(time.time())
            coll.insert(book)
        self.redirect("/recommended")   # 跳转


def run():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
#     foo()
    run()


