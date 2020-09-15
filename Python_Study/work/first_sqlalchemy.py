#!urs/bin/env python
#coding:utf-8


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import randint


DB_CONNECT_STRING = 'mysql+pymysql://root:123456@localhost/study'
engine = create_engine(DB_CONNECT_STRING, echo = False)
DB_Session = sessionmaker(bind = engine)
session = DB_Session()


def do_mysql():
    #直接使用SQL
    print(session.execute('show tables;').fetchall())
    print(session.execute('select * from fruits;').fetchall())
    
#ORM使用方式
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def init_db():
    BaseModel.metadata.create_all(engine)   #自动找到BaseModel子类并创建表
    
def drop_db():
    BaseModel.metadata.drop_all(engine)
    
class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(CHAR(30)) #or Column(String(30))

#使用
from sqlalchemy import or_, not_, func

def use_db():
#     session.execute('delete from user where true;')
    session.execute('truncate table user;')
    user = User(name = 'a')
    session.add(user)
    user = User(name = 'b')
    session.add(user)
    user = User(name = 'c')
    session.add(user)
    user = User()
    session.add(user)
    session.commit()
    
    query = session.query(User)
    print(query)    #显示SQL语句
    print(query.statement)  #同上
#     for user in query:      #遍历时查询
#         print(user.name)
    
    print(query.all())  #返回的是一个类似列表的对象
    print(query.first().name)   #记录不存在时，first()会返回None
    # print(query.one().name)   #不存在，或有多行记录时会抛出异常
    print(query.filter(User.id == 2).first().name)
    print(query.get(2).name)    #以主键获取，等效于上句
    print(query.filter('id=2').first().name)  #支持字符串
    
    query2 = session.query(User.name)
    print(query2.all()) #每行是个元组
    print(query2.limit(1).all())  #最多返回1条记录
    print(query2.offset(1).all())  #从第二条记录开始返回
    print(query2.order_by(User.name).all()) #空排在最前
    print(query2.order_by('name').all())
    print(query2.order_by(User.name.desc()).all())  #倒序
    print(query2.order_by('name desc').all())
    #SELECT "user".id AS user_id FROM "user" ORDER BY "user".name DESC, "user".id
    print(session.query(User.id).order_by(User.name.desc(), User.id).all())
    
    print(query2.filter(User.id == 1).scalar()) #如果有记录，返回第一条记录的第一个元素
    print(session.query('id').select_from(User).filter('id=1').scalar())
    print(query2.filter(User.id > 1, User.name != 'a').first()) #and
#     print(query2.filter(User.id > 1, User.name != 'a').scalar()) #and
    query3 = query2.filter(User.id > 1) #多次拼接filter也是and
    query3 = query3.filter(User.name != 'a')
    print(query3.first())
    print(query2.filter(or_(User.id == 1, User.id == 2)).all()) #or
    print(query2.filter(User.id.in_((1, 2))).all()) #in
    
    query4 = session.query(User.id)
    print(query4.filter(User.name == None).scalar())
    print(query4.filter('name is null').scalar())
    print(query4.filter(not_(User.name == None)).all()) #not
    print(query4.filter(User.name != None).all())
    print(query4.count())
    
    print(session.query(func.count('*')).select_from(User).scalar())
    print(session.query(func.count('1')).select_from(User).scalar())    #结果为4
    print(session.query(func.count(User.id)).scalar())
    #filter()中包含User，因此不需要指定表
    print(session.query(func.count('*')).filter(User.id > 0).scalar())
    print(session.query(func.count('*')).filter(User.name == 'a').limit(1).\
          scalar() == 1) #可以用limit()限制count()的返回数
    print(session.query(func.sum(User.id)).scalar())
    print(session.query(func.now()).scalar())   #func后可以跟任意函数名，只要该数据库支持
    print(session.query(func.current_timestamp()).scalar())
    print(session.query(func.md5(User.name)).filter(User.id == 1).scalar())
    
    query.filter(User.id == 1).update({User.name : 'c'})
    user = query.get(1)
    print(user.name)
    
    user.name = 'd'
    session.flush() #写数据库，但并不提交
    print(query.get(1).name)
    
    session.delete(user)
    session.flush()
    print(query.get(1))
    
    session.rollback()
    print(query.get(1).name)
    query.filter(User.id == 1).delete()
    session.commit()
    print(query.get(1))
    
#插入大批数据
#非ORM的方式，而ORM方式会花掉很长的时间
def insert_many():
    session.execute(
        User.__table__.insert(),
        [{'name' : randint(1, 100), 'age' : randint(1, 100)} for i in range(10000)]
    )
    
#SQL语句增加前缀
def prefix():
    session.query(User.name).prefix_with('HIGH_PRIORITY').all()
    session.execute(User.__table__.insert().prefix_with('IGNORE'), \
                    {'id' : 1, 'name' : 1}
                    )
    
#替换一个已有主键的记录
def replace_pk():
    user = User(id = 1, name = 'ooxx')
    session.merge(user)
    session.commit()
#或者使用MySQL的INSERT...ON DUPLICATE KEY UPDATE，需要用到@compiles装饰器。

#使用无符号整数
def unsigned_t():
    from sqlalchemy.dialects.mysql import INTEGER
    id = Column(INTEGER(unsigned = True), primary_key = True)
    
#字段名字为python关键字
def key_deal():
    from_ = Column('from', CHAR(10))
    
#获取字段长度
#Column会生成一个很复杂的对象，想获取长度比较麻烦
def get_column_length():
    return User.name.property.columns[0].type.length

#指定InnoDB以及使用utf-8编码
#最简单的方式时候修改数据的默认配置。可以在代码里指定
# class User2(BaseModel):
#     __table__args__ = {
#         'mysql_engine' : 'InnoDB',
#         'mysql_charset' : 'utf8'
#     }
    
#设置外键约束
from sqlalchemy import ForeignKey
class Friendship(BaseModel):
    __tablename__ = 'friendship'
    id = Column(Integer, primary_key = True)
    user_id1 = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    user_id2 = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    
def fk_do():
    session.query(User).delete()
    session.query(Friendship).delete()
    for i in range(100):
        session.add(User(id = i))
    session.flush() #或session.commit() 执行完后，user对象的id属性才可以访问（id是自增的）
    for i in range(60):
        session.add(Friendship(user_id1 = i, user_id2 = i))
    session.commit()
    session.query(User).filter(User.id < 50).delete()
    '''
    值得注意的，在Friendship表的两个字段中必须加入ondelete和onupdate约束。
    原因是删除user表的数据，可能会导致friendship的外键不指向一个真实存在的记录。
    在默认情况下，MySQL会拒绝这种操作，也就是RESTRICT。InnoDB还允许指定ON DELETE为
    CASCADE和SET NULL，前者除了删除，还有可能更改主键。这也会导致friendship的外键
    失效，于是相应就有ON UPDATE了。其中CASCADE编程了更新相应的外键，而不是删除。
    '''
    

#无法删除in操作查询出来的记录
def cannot_del():
    session.query(User).filter(User.id.in_((1, 2, 3))).delete() #不能通过
    session.query(User).filter(or_(User.id == 1, User.id == 2, User.id == 3)).delete()
    '''
    删除记录时，默认会尝试删除session中符合条件的对象，而in操作估计还不支持，于是就出错
    了。解决的办法就是删除时不进行同步，然后让session里所有实体都过期。如下：
    session.query(User).filter(User.id.in_((1, 2, 3))).\
    delete(synchronize_session = False)
    session.commit()    #or session.expire_all()
    此外，update操作也有同样的参数，如果后面立刻提交了，那么加上synchronize_session=
    False参数会更快。
    '''
    
#设置__abstract__属性
class BaseModel2(BaseModel):
    __abstract__ = True
    __table_args__ = {  #可以省掉子类的__table_args__了
        'mysql_engine' : 'InnoDB',
        'mysql_charset' : 'utf8'
    }
    #这种方法最简单，也可以继承出多个类
    
    
#正确使用事务
class User2(BaseModel):
    __tablename__ = 'user2'
    id = Column(Integer, primary_key = True)
    money = Column(DECIMAL(10, 2))
    
class TanseferLog(BaseModel):
    __tablename__ = 'tanseder_log'
    id = Column(Integer, primary_key = True)
    from_user = Column(Integer, ForeignKey('user2.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    to_user = Column(Integer, ForeignKey('user2.id', ondelete = 'CASCADE', onupdate = 'CASCADE'))
    amount = Column(DECIMAL(10, 2))
    
def bank_do():
    session.execute('drop table tanseder_log;')
    session.execute('drop table user2;')
    init_db()
    
    user = User2(money = 100)
    session.add(user)
    user = User2(money = 0)
    session.add(user)
    session.commit()
    
    #然后开两个session，同时进行两次转账操作。（每个session都是单独的）
    session1 = DB_Session()
    session2 = DB_Session()
    
    user1 = session1.query(User2).get(1)
    user2 = session1.query(User2).get(2)
    if user1.money >= 100:
        user1.money -= 100
        user2.money += 100
        session1.add(TanseferLog(from_user = 1, to_user = 2, amount = 100))
    
    user1 = session2.query(User2).get(1)
    user2 = session2.query(User2).get(2)
    if user1.money >= 100:
        user1.money -= 100
        user2.money += 100
        session2.add(TanseferLog(from_user = 1, to_user = 2, amount = 100))
    
    session1.commit()
    session2.commit()
    
    #check
    print(user1.money)          #0
    print(user2.money)          #100
    print(session.query(TanseferLog).count())   #2
    ##
    #两次都转账成功，但是只转走了一笔钱，这明显不科学。
    #可见MySQL InnoDB虽然支持事务，还需要手动加锁。
    ##
    
#首先试试读锁
'''
user1 = session1.query(User).with_lockmode('read').get(1)
user2 = session1.query(User).with_lockmode('read').get(2)
if user1.money >= 100:
    user1.money -= 100
    user2.money += 100
    session1.add(TanseferLog(from_user=1, to_user=2, amount=100))

user1 = session2.query(User).with_lockmode('read').get(1)
user2 = session2.query(User).with_lockmode('read').get(2)
if user1.money >= 100:
    user1.money -= 100
    user2.money += 100
    session2.add(TanseferLog(from_user=1, to_user=2, amount=100))
session1.commit()
session2.commit()

现在执行session1.commit()的时候，因为user1和user2都被session2加了读锁，所以会等待锁
被释放。超时以后，session1.commit()会抛出超时的异常，如果捕捉了的话，或者session2
在另一个进程，那么session2.commit()还是能正常提交的。在这种情况下，有一个事务肯定会
提交失败的，所以那些更改等于白做了。
接下来看看写锁，把上段代码中的read改成update即可。这次在执行select的时候就会被阻塞了：
user1 = session2.query(User).with_lockmode('update').get(1)
这样只要在超时期间内，session1完成了提交或回滚，那么session2就能正常判断user1.money
>= 100是否成立了。
由此可见，如果需要更改数据，最好加写锁。
那么什么时候用读锁呢？如果要保证事务运行期间，被读取的数据不被修改，自己也不去修改，
加读锁即可。
举例来说，假设我查询一个用户的开支记录（同时包含余额和转账记录），可以直接把user和
tanseder_log做个内连接。
但如果用户的转账记录特别多，我在查询前想先验证用户的密码（假设在user表中），确认相符
后才查询转账记录。而这两次查询的期间内，用户可能收到浏览一笔转账，导致他的money字段
被修改了，但我在展示给用户时，用户的余额仍然没有改变，这就不正常了。
而如果我在读取user时加了读锁，用户是无法收到转账的（因为无法被另一个事务加写锁来修改
money字段），这就保证不了不会查询出额外的tanseder_log记录。等我查询完两张表，释放了
读锁后，转账就可以继续进行了，不过我显示的数据在当时的确是正确和一致的。
另外需要注意的是，如果被查询的字段没有加索引的话，就会变成锁整张表了：
session1.query(User).filter(User.id > 50).with_lockmode('update').all()
session2.query(User).filter(User.id < 40).with_lockmode('update').all() # 不会被锁，因为 id 是主键

session1.rollback()
session2.rollback()

session1.query(User).filter(User.money == 50).with_lockmode('update').all()
session2.query(User).filter(User.money == 40).with_lockmode('update').all() # 会等待解锁，因为 money 上没有索引

要避免的话，可以这样：
money = Column(DECIMAL(10, 2), index = True)
另一个注意点是子事务。
InnoDB支持子事务（savepoint语句），可以简化一些逻辑。
例如有的方法是用于改写数据库的，它执行时可能提交了事务，但在后续的流程中却执行失败了，
却没法回滚那个方法中已经提交的事务。这时就可以把那个方法当成子事务来运行了：
def step1():
    # ...
    if success:
        session.commit()
        return True
    session.rollback()
    return False

def step2():
    # ...
    if success:
        session.commit()
        return True
    session.rollback()
    return False

session.begin_nested()
if step1():
    session.begin_nested()
    if step2():
        session.commit()
    else:
        session.rollback()
else:
    session.rollback()
此外，rollback一个子事务，可以释放这个子事务中获得的锁，提高并发性和降低死锁概率。
'''
    
    
#对一个字段进行自增操作
#最简单的办法就是获取时加上写锁
def auto_increment():
    user = session.query(User).with_lockmode('update').get(1)
    user.age += 1
    session.commit()
#如果不想多一次读的话，这样写也是可以的
'''
session.query(User).filter(User.id == 1).upodate(
    {User.age : Userage + 1}
)
session.commmit()
其实字段之间也可以做运算
session.query(User).filter(User.id == 1).update(
    {User.age : User.age + User.id}
)
'''

if __name__ == '__main__':
#     do_mysql()
    init_db()
#     use_db()
#     fk_do()
    bank_do()