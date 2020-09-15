# !/usr/bin/python
#coding:utf-8


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        conn = pymongo.MongoClient('localhost', 27017)
        self.db = conn.get_database('example')       # 数据库名
        tornado.web.Application.__init__(self, handlers, debug=False)

class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        db = self.application.db                      # 获取数据库
        collections = db.get_collection('words')      # 获取集合
        word_doc = collections.find_one({"word": word})
        if word_doc:
            word_doc.pop('_id')
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "%s: not found" % word})

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
    