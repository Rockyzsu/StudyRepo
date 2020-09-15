#！/usr/bin/python
#coding:utf-8


import json
import gevent
from gevent.queue import Queue, Empty
from gevent.pywsgi import WSGIServer

# WSGI是Web Server Gateway Interface的缩写。以层的角度来看，WSGI所在层的位置低于CGI。
# 但与CGI不同的是WSGI具有很强的伸缩性且能运行于多线程或多进程的环境下，这是因为WSGI
# 只是一份标准并没有定义如何去实现。实际上WSGI并非CGI，因为其位于web应用程序与web服
# 务器之间，而web服务器可以是CGI，mod_python（注：现通常使用mod_wsgi代替），FastCGI
# 或者是一个定义了WSGI标准的web服务器就像python标准库提供的独立WSGI服务器称为wsgiref。
# WSGI标准在PEP(注:Python Enhancement Proposal)3333中定义并被许多框架实现，其中包括
# 现广泛使用的django框架。


data_source = Queue()

def producer():
    while True:
        data_source.put_nowait('Hello World')
        gevent.sleep(1)
        
def ajax_endpoint(environ, start_response):
    # WSGI接口定义非常简单，它只要求开发者实现一个函数，就可以相应HTTP请求。
    # 本函数就符合WSGI标准的一个HTTP处理函数，它接收两个参数：environ——一个包含所有
    # HTTP请求信息的dict对象；start_response——一个发送HTTP响应的函数。
    status = '200 OK'
    headers = [
               ('Content-Type', 'application/json')
               ]
    start_response(status, headers)
    
    while True:
        try:
            datum = data_source.get(timeout=5)
            yield json.dumps(datum) + '\n'
        except Empty: pass

if __name__ == '__main__':
    gevent.spawn(producer)
    WSGIServer(('', 8000), ajax_endpoint).serve_forever()
    
    