#!urs/bin/env python
#coding:utf-8


from elasticsearch import Elasticsearch

# es = Elasticsearch('localhost')
es = Elasticsearch('10.18.15.9')
es.indices.create(index='megacorp', ignore=400)

def insert(data, id_):
    es.index(index='megacorp', doc_type='employee', body=data, id=id_)
    print('插入一条数据成功！index：%s，type：%s' % ('megacorp', 'employee'))
    
def insert_do():
    insert(
           {
            "first_name": "John",
            "last_name": "Smith",
            "age": 25,
            "about": "I love to go rock climbing",
            "interests": ["sports", "music"]
            }, 1
           )
    insert(
           {
            "first_name": "Jane",
            "last_name": "Smith",
            "age": 32,
            "about": "I like to collect rock albums",
            "interests": ["music"]
            }, 2
           )
    insert(
           {
            "first_name": "Douglas",
            "last_name": "Fir",
            "age": 35,
            "about": "I like to build cabinets",
            "interests": ["forestry"]
            }, 3
           )


def search_all(index_, type_):
    data = es.search(index=index_, doc_type=type_, body={"query":{"match_all":{}}})
    finally_data = [i['_source'] for i in data['hits']['hits']]
    for i in finally_data:
        print(i)

def search_do(id_):
    result = []
    data = es.get(index='megacorp', doc_type='employee', id=id_)
    data2 = es.get(index='socail_se2', doc_type='socail_base_se2', id='AVmtIB95zBhrkzFcj4ox')
    result.append(data)
    result.append(data2)
    print(result)
    
def search_do2():
    # DSL查询语句
    # http://localhost:9200/megacorp/employee/_search?q=last_name:Simth
    # http://localhost:9200/megacorp/employee/_search?{"query":{"match":{"last_name" : "Smith"}}}
    data = es.search(index="megacorp", body={"query":{"match":{'last_name' : 'Smith'}}})
    print(data)
    
def search_do3():
    # gt为greater than的缩写
    search_pattern = {'query': {'filtered': {'filter': {'range': {'age': {'gt': 30}}}}},
                      'query': {'match': {'last_name': 'Smith'}}
                      } # 或
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = [i['_source'] for i in data['hits']['hits']]
    for i in finally_data:
        print(i)
        
def search_full_text():
    # 全文搜索
    search_pattern = {'query': {'match': {'about': 'rock climbing'}}}
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = [i for i in data['hits']['hits']]
    for i in finally_data:
        print('权重：%f' % i['_score'], '数据：', i['_source'])
        
def search_by_phrase():
    # 短语搜索
    search_pattern = {'query': {'match_phrase': {'about': 'rock climbing'}}}
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = [i for i in data['hits']['hits']]
    for i in finally_data:
        print('权重：%f' % i['_score'], '数据：', i['_source'])
        
def search_by_highlight():
    # 高亮搜索，在浏览器中实验未高亮
    search_pattern = {'query': {'match_phrase': {'about': 'rock climbing'}},
                      'highlight': {'fields': {'about': {}}}}
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = [i for i in data['hits']['hits']]
    for i in finally_data:
        print('权重：%f' % i['_score'], '数据：', i['_source'])
        
def search_analyze():
    # 分析
    # 所有职员中最大的共同点（兴趣爱好）
    search_pattern = {'aggs': {'all_interests': {'terms': {'field': 'interests'}}}}
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = data['aggregations']['all_interests']['buckets']
    for i in finally_data:
        print('关键字：%s，次数：%d' % (i['key'], i['doc_count']))
        
def search_analyze2():
    # 所有姓Smith的人的最大的共同点（兴趣爱好）
    search_pattern = {'query': {'match': {'last_name': 'Smith'}},
                      'aggs': {'all_interests': {'terms': {'field': 'interests'}}}}
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = data['aggregations']['all_interests']['buckets']
    for i in finally_data:
        print('关键字：%s，次数：%d' % (i['key'], i['doc_count']))
        
def search_analyze3():
    # all_interests聚合允许分级汇总。统计每种兴趣下职员的平均年龄
    search_pattern = {'aggs': {'all_interests': {'terms': {'field': 'interests'},
                                                 'aggs': {'avg_age': {'avg': {'field': 'age'}}}}
                               }
                      }
    data = es.search(index="megacorp", body=search_pattern)
    finally_data = data['aggregations']['all_interests']['buckets']
    for i in finally_data:
        print('关键字：%s，次数：%d，平均年龄：%4.2f' % (i['key'], i['doc_count'], i['avg_age']['value']))
    

if __name__ == '__main__':
#     search_all('message_index', 'message_type')
#     insert_do()
    search_do(1)
#     search_do2()
#     search_do3()
#     search_full_text()
#     search_by_phrase()
#     search_by_highlight()
#     search_analyze()
#     search_analyze2()
#     search_analyze3()
    