#!urs/bin/env python
#coding:utf-8


import pymongo

def connect_db():
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.get_database('example')
    # 集合widgets在数据库中不存在，这样会创建一个
    widgets = db['widgets'] # or widgets = db.widgets
    widgets.insert({"foo": 'bar'})
    widgets.insert({"name": "flibnip", "description": "grade-Aindustrial flibnip", "quantity": 3})
    widgets.insert({"name":"smorkeg","description":"forexternaluse only", "quantity": 4})
    widgets.insert({"name": "clobbasker", "description": "properties available on request", "quantity": 2})

    line =widgets.find_one({"name": "flibnip"})
    print(line)
    
    # save
    line['quantity'] = 4
    widgets.save(line)
    
    # 遍历
    for doc in widgets.find():
        print(doc)
    # 如果我们希望获得文档的一个子集，传递一个字典参数。比如找到那些quantity键的值为
    # 4的集合
    for doc in widgets.find({'quantity': 4}):
        print(doc)
        
    # 删除
    widgets.remove({"name": "flibnip"})
    for doc in widgets.find():
        print(doc)
        

# 数据准备
def foo():
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.get_database('example')
    db.words.insert({"word": "oarlock", "definition": "A deviceattached to a rowboat to hold the oars in place"})
    db.words.insert({"word": "seminomadic", "definition": "Onlypartially nomadic"})
    db.words.insert({"word": "perturb", "definition": "Bother,unsettle, modify"})
    conn.close()
    
# 数据准备2
def foo2(): pass


if __name__ == '__main__':
#     connect_db()
    foo()