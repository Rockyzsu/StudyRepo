#!urs/bin/env python
#coding:utf-8


import re
# from collections import Iterable
#Iterable并不能判断re模块finditer方法返回的对象是否可迭代，所有都是True
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import Column, MetaData, Table
from sqlalchemy.types import Integer, TEXT, VARCHAR


DB_CONNECT_STRING = 'mysql+pymysql://root:123456@localhost/work?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, 
#                        echo = True  #echo表示是否输出log
                       )
metadata = MetaData()   #跟踪表属性

dajiyuan_table = Table(
    'dajiyuan',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('title', TEXT),
    Column('author', TEXT),
    Column('content', TEXT),
    Column('date', TEXT),
    Column('tags', TEXT),
    Column('others', TEXT),
    Column('jour', TEXT)
)

dajiuyuan_table_filter = Table(
    'dajiyuan_filter',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('dajiyuan_id', Integer),
    Column('key', VARCHAR(128))
)
# metadata.create_all(engine) #在数据库中生成表


class Dajiyuan(object): pass     #创建一个映射类
class DajiyuanFilter(object): pass

mapper(Dajiyuan, dajiyuan_table)  #把表映射到类
mapper(DajiyuanFilter, dajiuyuan_table_filter)
Session = sessionmaker()        #创建一个自定义了的Session类
Session.configure(bind = engine)#将创建的数据库连接关联到这个session
session = Session()

def get_all():
    query = session.query(Dajiyuan)  
    index_ = 1
    while True: #连续的
        row = query.get(index_)
        if row:
            yield row
        else:
            break
        index_ += 1

def insert_result(tag, id_):
    #将结果插入新表
    f = DajiyuanFilter()
    f.dajiyuan_id = id_
    f.key = tag
    session.add(f)
    
def run(row):
    def only_split():
        tags = row.tags[1:-1]   #去掉两端的中括号
        tags = tags.split(', ')
        tags = list(map(lambda x: x[1:-1].strip(), tags)) #去掉两边引号和空字符
        return tags
        
    tags = only_split()
    print(tags)
    for tag in tags:
        insert_result(tag, row.id)
    

if __name__ == '__main__':
    for row in get_all():
        run(row)
    session.commit()
    print('提交完成！')