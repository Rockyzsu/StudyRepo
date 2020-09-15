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
    'minghui',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('title', TEXT),
    Column('author', TEXT),
    Column('content', TEXT),
    Column('date', TEXT),
    Column('tags', TEXT),
    Column('others', TEXT)
)

minghui_table_filter = Table(
    'minghui_author',
    metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('minghui_id', Integer),
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
    author = author.strip()
    print(author)
    f = MingHuiFilter()
    f.minghui_id = id_
    f.author = author
    session.add(f)
    
author_pattern = re.compile(r'(?<=文[:|：])[\s]*.+')
def run(row):
    def only_search():
        m = author_pattern.search(row.author)
        if m:
            return m.group()
        return ''
        
    if row.author.strip():
        author = only_search()
        if author:
            insert_result(author, row.id)
        

def main():
    for row in get_all():
        run(row)
    session.commit()
    print('提交完成！')
    
def test():
    author_pattern = re.compile(r'(?<=文[:|：])[\s]*.+')
    string = "文： 山西大法弟子 我"
    m = author_pattern.search(string)
    if m:
        print(m.group())

if __name__ == '__main__':
    main()
#     test()
