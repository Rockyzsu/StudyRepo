#!urs/bin/env python
#coding:utf-8


import json
import random
from gevent import pywsgi, sleep
from geventwebsocket.handler import WebSocketHandler


class WebSocketApp(object):
    # Send random data to the websocket
    def __call__(self, environ, start_response):
        ws = environ['wsgi.websocket']
        x = 0
        while True:
            data = json.dumps({'x': x, 'y': random.randint(1, 5)})
            ws.send(data)
            x += 1
            sleep(0.5)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('', 10000), WebSocketApp(), handler_class=WebSocketHandler)
    server.serve_forever()