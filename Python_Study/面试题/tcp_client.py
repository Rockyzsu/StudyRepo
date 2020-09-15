#!usr/bin/env python
#coding:utf-8

import socket
import time

sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',8001))
time.sleep(2)
sock.send(b'1')
print(sock.recv(1024))
sock.close()
