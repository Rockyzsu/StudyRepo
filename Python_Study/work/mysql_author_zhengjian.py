#!urs/bin/env python
#coding:utf-8


import re
# from collections import Iterable
#Iterable并不能判断re模块finditer方法返回的对象是否可迭代，所有都是True
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import Column, MetaData, Table
from sqlalchemy.types import Integer, TEXT, VARCHAR, BLOB


DB_CONNECT_STRING = 'mysql+pymysql://root:123456@localhost/work?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, 
#                        echo = True  #echo表示是否输出log
                       )
metadata = MetaData()   #跟踪表属性

minghui_table = Table(
    'zhengjian',
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

minghui_table_filter = Table(
    'zhengjian_author',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('zhengjian_id', Integer),
    Column('author', VARCHAR(128)),
)
# metadata.create_all(engine) #在数据库中生成表


class MingHui(object): pass     #创建一个映射类
class MingHuiFilter(object): pass

mapper(MingHui, minghui_table)  #把表映射到类
mapper(MingHuiFilter, minghui_table_filter)
Session = sessionmaker()        #创建一个自定义了的Session类
Session.configure(bind = engine)#将创建的数据库连接关联到这个session
session = Session()
    



def get_all():
    #简单的理解就是select()的支持ORM的替代方法，可以接受任意组合的class/column表达式
    query = session.query(MingHui)  
    index_ = 1
    while True: #连续的
        row = query.get(index_)
        if row:
            yield row
        else:
            break
        index_ += 1
        
def insert_result(author, id_):
    #将结果插入新表
    print(author)
    f = MingHuiFilter()
    f.zhengjian_id = id_
    f.author = author
    session.add(f)
    
def run(row):
    def only_split():
        authors = row.author.split(' ')
        authors = filter(lambda x: x, authors)
        authors = list(map(lambda x: x.strip(), authors))
        return authors
        
    if row.author:
        author_list = only_split()
        for author in author_list:
            insert_result(author, row.id)
        

def main():
    for row in get_all():
        run(row)
    session.commit()
    print('提交完成！')
    

if __name__ == '__main__':
    main()
