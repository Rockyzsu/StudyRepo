#!urs/bin/env python
#coding:utf-8


from tornado.gen import coroutine
from tornado.web import asynchronous
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient

class AsyncHandler(RequestHandler):
    @asynchronous
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch("http://baidu.com",
                          callback=self.on_fetch)

    def on_fetch(self, response):
        print(response.status_code)
        self.render("template.html")
        
        
# 这个和上面是一样的
class GenAsyncHandler(RequestHandler):
    @coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://baidu.com")
        print(response.status_code)
        self.render("template.html")
        






if __name__ == '__main__':
    async_fetch_future('http://baidu.com')