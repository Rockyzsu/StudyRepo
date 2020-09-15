# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月5日
    @author: xiongqiao
    @attention：
'''

import logging
from logging.handlers import RotatingFileHandler


#定义一个RotatingFileHandler，最大备份5个日志文件，每个日志文件最大10M
Rthandler = RotatingFileHandler('myapp.log', maxBytes = 10 * 1024 * 1024, backupCount = 5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)