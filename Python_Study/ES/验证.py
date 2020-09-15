#!urs/bin/env python
#coding:utf-8


import re
import pymssql

table_name_p = re.compile(r'Table[a-zA-Z0-9_]+')
table_count_p = re.compile(r'(?<=有)\d+(?=行)')

def get_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                break
        
def get_data_tmp():
    a = [
    '[2017-01-16 10:06:00] INFO [console:27] 数据表Table_163com236已经导入完成，共有559102行。',
    '[2017-01-16 10:06:10] INFO [console:27] 数据表Table_163com237已经导入完成，共有559102行。',
    '[2017-01-16 10:08:15] INFO [console:27] 数据表Table_dianshang_huwai已经导入完成，共有642925行。',
    '[2017-01-16 10:09:09] INFO [console:27] 数据表Table_dianshang_gaizhuang已经导入完成，共有662860行。',
    '[2017-01-16 10:13:19] INFO [console:27] 数据表Table_163com562已经导入完成，共有935018行。',
    '[2017-01-16 10:14:34] INFO [console:27] 数据表Table_163com410已经导入完成，共有1000000行。'
    ]
    for i in a:
        yield i

def get_all_tables():
    # 获得所有表名和表名对应的行数 SQL Server
    conn = pymssql.connect(database = 'socail', user = 'twodept', 
                           password = 'twodept',host = '192.168.1.106', port = 1433
                           )
    cur = conn.cursor()
    # 查询所有表名，以及表名对应的行数
    sql = '''
    SELECT a.name, b.rows
    FROM sysobjects AS a INNER JOIN sysindexes AS b ON a.id = b.id
    WHERE (a.type = 'u') AND (b.indid IN (0, 1))
    ORDER BY a.name,b.rows DESC;
    '''
    cur.execute(sql)
    tables = cur.fetchall()
    return dict(tables)
    

if __name__ == '__main__':
    all_ = get_all_tables()
    n_true = 0
    n_false = 0
    for line in get_data('./import_dbase_information.log'):
#     for line in get_data_tmp():
        m1 = table_name_p.search(line)
        m2 = table_count_p.search(line)
        if m1 and m2:
            table_name, table_count = m1.group(), int(m2.group())
        else:
            continue
        if table_name in all_:
            bool_yes = 'True' if table_count == all_[table_name] else 'False'
            if bool_yes == 'True':
                n_true += 1
            else:
                n_false += 1
            print('表%s有%d行，数据库里实际有%d行，结果：%s。' % 
                  (table_name, table_count, all_[table_name], bool_yes)
                  )
        else:
            print('表%s在数据库中不存在！' % table_name)
    print('汇总：总共有%d张表，已经导入%d张，%d张数据正常，%d张不正常。' % (len(all_), n_true + n_false, n_true, n_false))
            