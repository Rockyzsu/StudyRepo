

import json
import os
import os.path
from pymongo import MongoClient

# 1. 连接数据库
client = MongoClient('localhost', 27017)
db_name = 'work'
db = client[db_name]
collection = db['task']

# 2. 插入数据
# save() VS insert()
# mongodb的save和insert函数都可以向collection里插入数据，但两者是有两个区别：
# 一、save函数实际就是根据参数条件,调用了insert或update函数.如果想插入的数据对象存在,insert函数会报错,\
#   而save函数是改变原来的对象;如果想插入的对象不存在,那么它们执行相同的插入操作.这里可以用几个字来概括它
# 们两的区别,即所谓"有则改之,无则加之".
# 二、insert可以一次性插入一个列表，而不用遍历，效率高， save则需要遍历列表，一个个插入。

# 3. 更新数据
# 对于单个数据来说，可以更新后使用save方法
# update(criteria, objNew, upsert, mult)
#     criteria: 需要被更新的条件表达式
#     objNew: 更新表达式
#     upsert: 如目标记录不存在，是否插入新文档。
#     multi: 是否更新多个文档。
# collection.update({'gid':last_gid, 'time':l_date},
#                  {'$set':{'gid':last_gid},
#                   '$set':{'time':l_date},
#                   '$addToSet':{'categories':category_data}},
#                  upsert=True)

# 4. 删除数据
# collection.drop()   # 删除集合
# remove(self, spec_or_id=None, safe=None, multi=True, **kwargs)
# remove()          # 用于删除单个或全部文档，删除后的文档无法恢复。
# id = collection.find_one({'_id': '国家电网-一线风采'})
# collection.remove(id)           # 根据id删除一条记录
# collection.remove()             # 删除集合里的所有记录
# collection.remove({'yy': 5})    # 删除yy=5的记录

# 5. 查询
def mongo_select():
    # 条件查询符
    # "$lt" == == == == == == == == == = > "<"
    # "$lte" == == == == == == == == == > "<="
    # "$gt" == == == == == == == == == = > ">"
    # "$gte" == == == == == == == == == > ">="
    # "$ne" == == == == == == == == == = > "!="
    # for u in collection.find({'delay': {'$gt': 1}}):
    #     print(u)

    # 查询特定键
    # select _id, ajax from task where delay > 1;
    for u in collection.find({'delay': {'$gt': 1}}, ['_id', 'ajax', 'delay']):
        print(u)


# 5.3 排序
def mongo_sort():
    # select _id, delay from task order by delay asc;
    # -1参数表示降序
    # collection.find(...).sort([(key1, 1 or -1), (key2, 1 or -1), ...])
    for u in collection.find({}, ['delay']).sort([('delay', 1)]):
        print(u)
    # 另一种写法
    # collection.find([condition], sort=[(key1, 1 or -1), (key2, 1 or -1), ...])


# 5.4 从第几行开始读取（SLICE），读取多少行（LIMIT）
def mongo_slice_limit():
    # select * from task limit 2, 3
    # collection.find(skip=2, limit=3)
    # collection.find()[2:5] 切片，这样是全部读取出来了，再切片，并不是真正的LIMIT
    for u in collection.find().skip(2).limit(3):
        print(u)

    # 另外地
    # skip和limit可以单独地使用，skip单独使用即表示从哪儿开始，一直到集合尾结束
    # limit单独使用即表示从第一个（索引0）开始，读取多少个结束


# 5.5 多条件查询
def mongo_more_conditions():
    # select * from task where delay between 2 and 20 and depth_limit=0;
    for u in collection.find({'depth_limit': 0, 'delay': {'$gte': 2, '$lte': 20}}):
        print(u)


# 5.6 IN
def mongo_in():
    # $in #nin
    # select * from task where delay in (1, 2, 3, 4, 5);
    for u in collection.find({'delay': {'$in': (1, 2, 3, 4, 5)}}):
        print(u)


# 5.7 count() 统计总数
# collection.find().count()

# 5.8 $exists
# 判断字段是否存在

# 5.9 正则表达式
# $regex
def mongo_regex():
    for u in collection.find({'_id': {'$regex': r'^乐山.+'}}):
        print(u)


# 5.10 多路径的元素值匹配
def mongo_many_path():
    # Document 采取 JSON-like 这种层级结构，因此我们可以直接用嵌入(Embed)代替传统关系型数据库的关
    # 联引用(Reference)。
    # MongoDB 支持以 "." 分割的 namespace 路径，条件表达式中的多级路径须用引号

    # 如果键里面包含数组，只需简单匹配数组属性是否包含该元素即可查询出来
    # db.集合名.find_one({'address': "address1"})  # address 是个数组，匹配时仅需包含有即可
    # # 查询结果如：{"_id" : ..., "name" : "user1", "address" : ["address1", "address2"]}

    # 条件表达式中的多级路径须用引号，以“.”分隔
    # print(collection.find_one({'headers.User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'}))

    # 多级路径的更新
    # db.集合名.update({'im.qq': 12345678}, {'$set': {'im.qq': 12345}})

    # 查询包含特定键的
    # for u in db.users.find({"im.qq": {'$exists': True}}, {"im.qq": 1}):
    #     print(u)
    # 显示如： { "_id" : ..., "im" : { "qq" : 12345 } }

    # for u in db.users.find({'data': "abc"}):
    #     print(u)
    # 显示如： { "_id" : ..., "name" : "user8", "data" : [ { "a" : 1, "b" : 10 }, 3, "abc" ] }
    # for u in db.users.find({'data': {'$elemMatch': {'a': 1, 'b': {'$gt': 5}}}}):
    #     print(u)
    # 显示如： { "_id" : ..., "name" : "user8", "data" : [ { "a" : 1, "b" : 10 }, 3, "abc" ] }
    # {data: "abc"}仅简单匹配数组属性是否包含该元素。$elemMatch则可以处理更复杂的元素查找条件。
    # 当然也可以写成如下方式：
    # db.集合名.find({"data.a": 1, "data.b": {'$gt': 5}})

    # 对数组, 还可以直接使用序号进行操作：
    # db.集合名.find({"data.1": 3})  # 序号从0开始

    # 如集合的一列内容
    # {"classifyid": "test1",
    #  "keyword": [
    #      {"name": 'test1',  # 将修改此值为 test5 (数组下标从0开始,下标也是用点)
    #       "frequence": 21,
    #       },
    #      {"name": 'test2',  # 子表的查询，会匹配到此值
    #       "frequence": 50,
    #       },
    #  ]
    #  }
    # 子表的修改(子表的其它内容不变)
    # db.集合名.update({"classifyid": "test1"}, {"$set": {"keyword.0.name": 'test5'}})
    # 子表的查询
    # db.集合名.find({"classifyid": "test1", "keyword.0.name": "test2"})
    return


# 6. 操作
# $all，判断数组属性是否包含全部条件
# db.users.find({'data': {'$all': [2, 3, 4]}})
# 显示： { "_id" : ..., "name": "user3", "data": [1, 2, 3, 4, 5, 6, 7]}

# $size，匹配数组属性元素数量
# db.users.find({'data': {'$size': 3}})
# 显示：{ "_id" : ..., "name": "user4", "data": [1, 2, 3]}

# $type，判断属性类型
# db.users.find({'t': {'$type': 1}})
# 类型值:
# double:1
# string: 2
# object: 3
# array: 4
# binary data: 5
# object id: 7
# boolean: 8
# date: 9
# null: 10
# regular expression: 11
# javascript code: 13
# symbol: 14
# javascript code with scope: 15
# 32-bit integer: 16
# timestamp: 17
# 64-bit integer: 18
# min key: 255
# max key: 127

# $not，取反

# $unset和$set相反，表示移除文档属性
# for u in db.users.find({'name':"user1"}):
#     print(u)
# 显示如： { "_id" : ...), "name" : "user1", "age" : 15, "address" : [ "address1", "address2" ] }
# db.users.update({'name':"user1"}, {'$unset':{'address':1, 'age':1}})
# for u in db.users.find({'name':"user1"}):
#     print(u)
# 显示如： { "_id" : ..., "name" : "user1" }

# $push和$pushALl都是向数组属性添加元素
# for u in db.users.find({'name':"user1"}):
#     print(u)
# 显示如： { "_id" : ..., "age" : 15, "name" : "user1" }
# db.users.update({'name':"user1"}, {'$push':{'data':1}})
# for u in db.users.find({'name':"user1"}):
#     print(u)
# 显示如： { "_id" : ..., "age" : 15, "data" : [ 1 ], "name" : "user1" }
# db.users.update({'name':"user1"}, {'$pushAll':{'data':[2,3,4,5]}})
# for u in db.users.find({'name':"user1"}):
#     print(u)
# 显示如： { "_id" : ...), "age" : 15, "data" : [ 1, 2, 3, 4, 5 ], "name" : "user1" }

# $addToSet: 和 $push 类似，不过仅在该元素不存在时才添加 (Set 表示不重复元素集合)。
# db.users.update({'name':"user2"}, {'$unset':{'data':1}})
# db.users.update({'name':"user2"}, {'$addToSet':{'data':1}})
# db.users.update({'name':"user2"}, {'$addToSet':{'data':1}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 1 ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$push':{'data':1}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 1, 1 ], "name" : "user2" }
# 要添加多个元素，使用 $each。
# db.users.update({'name':"user2"}, {'$addToSet':{'data':{'$each':[1,2,3,4]}}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： {'age': 12, '_id': ..., 'data': [1, 1, 2, 3, 4], 'name': 'user2'}
# 貌似不会自动删除重复

# $each添加多个元素用
# db.users.update({'name':"user2"}, {'$unset':{'data':1}})
# db.users.update({'name':"user2"}, {'$addToSet':{'data':1}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 1 ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$addToSet':{'data':{'$each':[1,2,3,4]}}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： {'age': 12, '_id': ..., 'data': [1, 2, 3, 4], 'name': 'user2'}
# db.users.update({'name':"user2"}, {'$addToSet':{'data':[1,2,3,4]}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 1, 2, 3, 4, [ 1, 2, 3, 4 ] ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$unset':{'data':1}})
# db.users.update({'name':"user2"}, {'$addToSet':{'data':[1,2,3,4]}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ [1, 2, 3, 4] ], "name" : "user2" }

# $pop: 移除数组属性的元素(按数组下标移除)，$pull 按值移除，$pullAll 移除所有符合提交的元素。
# db.users.update({'name':"user2"}, {'$unset':{'data':1}})
# db.users.update({'name':"user2"}, {'$addToSet':{'data':{'$each':[1, 2, 3, 4, 5, 6, 7, 2, 3 ]}}})
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 1, 2, 3, 4, 5, 6, 7, 2, 3 ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$pop':{'data':1}}) # 移除最后一个元素
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 1, 2, 3, 4, 5, 6, 7, 2 ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$pop':{'data':-1}}) # 移除第一个元素
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 2, 3, 4, 5, 6, 7, 2 ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$pull':{'data':2}}) # 移除全部 2
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 3, 4, 5, 6, 7 ], "name" : "user2" }
# db.users.update({'name':"user2"}, {'$pullAll':{'data':[3,5,6]}}) # 移除 3,5,6
# for u in db.users.find({'name':"user2"}):
#     print(u)
# 显示： { "_id" : ..., "data" : [ 4, 7 ], "name" : "user2" }

# $where: 用 JS 代码来代替有些丑陋的 $lt、$gt。
# MongoDB 内置了 Javascript Engine (SpiderMonkey)。可直接使用 JS Expression，甚至使用 JS Function
# 写更复杂的 Code Block。
# db.users.remove() # 删除集合里的所有记录
# for i in range(10):
# db.users.insert({'name':"user" + str(i), 'age':i})
# for u in db.users.find():
#     print(u)
# for u in db.users.find().where("this.age > 7 || this.age < 3"):
# 使用自定义的 function, javascript语法的
# for u in db.users.find().where("function() { return this.age > 7 || this.age < 3;}")
# for u in db.users.find({"$where":"this.age > 7 || this.age < 3"}):
#     print(u)
# 显示如下：
# {'age': 0.0, '_id': ObjectId('4c47b3372a9b2be866da226e'), 'name': 'user0'}
# {'age': 1.0, '_id': ObjectId('4c47b3372a9b2be866da226f'), 'name': 'user1'}
# {'age': 2.0, '_id': ObjectId('4c47b3372a9b2be866da2270'), 'name': 'user2'}
# {'age': 8.0, '_id': ObjectId('4c47b3372a9b2be866da2276'), 'name': 'user8'}
# {'age': 9.0, '_id': ObjectId('4c47b3372a9b2be866da2277'), 'name': 'user9'}


if __name__ == '__main__':
    # mongo_select()
    # mongo_sort()
    # mongo_slice_limit()
    # mongo_more_conditions()
    # mongo_in()
    # mongo_regex()
    mongo_many_path()

    # shutdown
    client.close()