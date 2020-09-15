#!urs/bin/env python
#coding:utf-8

# 日志记录模块，用于记录程序运行时的错误等日志

import json
import logging.config
        

class MulLogger(object):
    '''多个进程写日志
    BUG：未测试是否真的进程安全
    '''
    def __init__(self, category='console'):
        config_file = './logging.conf'
        with open(config_file, 'r') as f:
            data = f.read()
        config = json.loads(data)
        logging.config.dictConfig(config)
        self.logger = logging.getLogger(category)
        
    # 下面的五个方法为logging的五个日志级别，不再一一赘述
    def debug(self, msg):
        self.logger.debug(msg)
        
    def info(self, msg):
        self.logger.info(msg)
        
    def warnning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
        
    def critical(self, msg):
        self.logger.critical(msg)
    
    
def test():
    logger = MulLogger()
    logger.debug('asdasd')
    logger.info('zxczxc')


if __name__ == '__main__':
    test()