#!urs/bin/env python
#coding:utf-8

# 实现从一个数据库里读取所有表的数据并插入到Elasticsearch数据库
# MySQL、SQLServer、PostgreSQL

import json
import logging
from collections import Iterable
from multiprocessing import Pool
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import RequestError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ES.db_logging import MulLogger
logger = MulLogger()

ONECE = 2000

def config():
    # 配置读取
    with open('config.json', 'r') as f:
        data = f.read()
    return json.loads(data)
conf = config()

################################################################################
# 连接数据库
DB_CONNECT_STRING = conf['db_choice'] + '+' + conf['db_engine'] + '://' + \
conf['db_account'] + ':' + conf['db_password'] + '@' + conf['db_host'] + ":" + conf["db_port"] +'/' + \
conf['db_name'] + '?' + 'charset=' + conf['db_charset']
engine = create_engine(DB_CONNECT_STRING, echo = False)
DB_Session = sessionmaker(bind = engine)
session = DB_Session()

################################################################################
mapping = {
  "settings":{
      "number_of_shards": 5,     # 分片数
      "number_of_replicas": 1    # 副本数
  },
  "mappings":{
      "message_type":{          # 表名
                "_all": { "analyzer": "keyword", "index": "not_analyzed"}
            }
        }
}

es = Elasticsearch(conf['elasticsearch_host'])
try:
    es.indices.create(index=conf['elasticsearch_index'], body=mapping)
except RequestError as e:
    logger.warnning('索引已经存在，或者模板错误。')
################################################################################

def wash_mobile(row):
    mobile = row.get('mobile')
    if mobile:
        mobile = mobile.split(',')
        row['mobile'] = [i.strip() for i in mobile]
    tel = row.get('tel')
    if tel:
        mobile = mobile.split(',')
        row['tel'] = [i.strip() for i in tel]
    return row

def get_all_tables():
    # 获得所有表名
    tables = session.execute(conf['db_get_all_tables']).fetchall()
    tables = list(tables)
    tables.sort()
    return tables

def get_one_table_data(table_name):
    # 获得一张表的所有数据
    if isinstance(table_name, Iterable):
        table_name = table_name[0]
    if 'Table_jingwai_9400W_24' == table_name:      # 异常表
        return []
    cur = session.execute('select * from %s;' % table_name)
    while True:
        rows = cur.fetchmany(ONECE)
        if not rows:
            break
        for row in rows:
            row = dict(row.items())
            row = wash_mobile(row)
            yield row
        
def insert_to_elasticsearch(data):
    # 单个插入数据到elasticsearch数据库
    if not data:
        return
    es.index(index=conf['elasticsearch_index'], 
             doc_type=conf['elasticsearch_type'], 
             body=data
             )
    
def insert_to_elasticsearch_bulk(data):
    # 批量插入
    bulk(es, data, index=conf['elasticsearch_index'], 
        doc_type=conf['elasticsearch_type'], 
        raise_on_error=True
        )
    
def go(table_name):
    # 每张表的读取以及插入到目标数据库
    rows = []   # 数据容器
    num = 0     # 循环计数器
    for row in get_one_table_data(table_name):
        rows.append(row)
        num += 1
        if not num % ONECE:
            try:
                insert_to_elasticsearch_bulk(rows)
            except:
                logger.error('错误的表：%s，错误的行：[%d-%d]' % (table_name, num - ONECE, num))
                num -= ONECE
            finally:
                rows.clear()
        
    # 扫尾-数据不足或数据有余数
    if rows:
        try:
            insert_to_elasticsearch_bulk(rows)
        except:
            logger.error('错误的表：%s，错误的行：[%d-%d]' % (table_name[0], num - len(rows), num))
        finally:
            num -= len(rows)
            del rows
    if num:
        logger.info('数据表%s已经导入完成，共有%d行。' % (table_name[0], num))
            

def run_with_pool(iterable_data):
    # 多个进程同时运行
    pool = Pool(processes=10)
    for data in iterable_data:
        pool.apply_async(go, (data,))
    pool.close()
    pool.join()
    

def run_one():
    # 单个测试执行
    data_list = []
    n = 0
    for table in get_all_tables():
        for row in get_one_table_data(table):
            data_list.append(row)
            if not n % ONECE and n:
                try:
                    insert_to_elasticsearch_bulk(data_list)
                    print(n)
                    data_list.clear()
                except:
                    logging.error('错误的数据1')
            n += 1
    if data_list:
        try:
            insert_to_elasticsearch_bulk(data_list)
            print(n + len(data_list))
        except:
            logging.error('错误的数据2')
        finally:
            data_list.clear()


if __name__ == '__main__':
    run_with_pool(get_all_tables())
#     run_one()
    