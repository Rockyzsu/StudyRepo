# !/usr/bin/python
#coding:utf-8

'''
    Created on 2016年8月5日
    @author: xiongqiao
    @attention：
'''

def log_test02():  
    import logging
    import logging.config
    
    CONF_LOG = "./logging.conf"  
    logging.config.fileConfig(CONF_LOG);    # 采用配置文件  
    logger = logging.getLogger("xzs")  
    logger.debug("Hello xzs")  
      
    logger = logging.getLogger()  
    logger.info("Hello root")  
      
if __name__ == "__main__":  
    log_test02()