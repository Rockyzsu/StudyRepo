#!urs/bin/env python
#coding:utf-8

from gevent.server import StreamServer


def handle(socket, address):
    socket.send(b'Hello from a telnet!\n')
    for i in range(5):
        socket.send(bytes(str(i) + '\n', 'utf-8'))
    socket.close()

if __name__ == '__main__':
    server = StreamServer(('localhost', 5000), handle)
    print('服务器启动！')
    server.serve_forever()