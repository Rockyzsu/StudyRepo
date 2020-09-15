#!urs/bin/env python
#coding:utf-8


import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import Column, MetaData, Table
from sqlalchemy.types import Integer, TEXT, VARCHAR

from others.jieba_split import jieba_split 


DB_CONNECT_STRING = 'mysql+pymysql://root:123456@localhost/work?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, 
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



class DaJiYuan(object): pass     #创建一个映射类
class DaJiYuanFilter(object): pass

mapper(DaJiYuan, dajiyuan_table)  #把表映射到类
Session = sessionmaker()        #创建一个自定义了的Session类
Session.configure(bind = engine)#将创建的数据库连接关联到这个session
session = Session()
    

def get_all():
    #简单的理解就是select()的支持ORM的替代方法，可以接受任意组合的class/column表达式
    query = session.query(DaJiYuan)  
    index_ = 182
    while True: #连续的
        row = query.get(index_)
        if row:
            result = jieba_split(row.content)
            try:
                query.filter(DaJiYuan.id == index_).update({DaJiYuan.content : result})
            except:
                print('异常%d！' % index_)
        else:
            break
        if not (index_ % 1000 and index_ != 0):
            print('已经更新%d条！' % index_)
        index_ += 1
    
if __name__ == '__main__':
    get_all()
    session.commit()
    print('完成！')
