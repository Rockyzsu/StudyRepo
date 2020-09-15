#!usr/bin/env python
#coding:utf-8

import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('localhost',8001))
sock.listen(5)
while True:
    connection,address =sock.accept()
    print('一个客户端连接进来了！')
    try:
        connection.settimeout(5)
        buf =connection.recv(1024)
        if buf == '1':
            connection.send(b'welcome to server!')
        else:
            connection.send(b'please go out!')
    except socket.timeout:
        print('time out')
        connection.close()
