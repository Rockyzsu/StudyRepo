
from sqlalchemy import create_engine  
engine=create_engine('sqlite:///:memory:',echo=True)  
  
from sqlalchemy import Table,Column,Integer,String,MetaData,ForeignKey  
metadata=MetaData()  
  
users_table=Table('users',metadata,  
  Column('id',Integer,primary_key=True),  
  Column('name',String),  
  Column('fullname',String),  
    Column('password',String)  
)  
  
metadata.create_all(engine)  
  
class User(object):  
    def __init__(self,name,fullname,password):  
        self.name=name  
        self.fullname=fullname  
        self.password=password  
    def __repr__(self):  
        return "<User('%s','%s','%s')>" % (self.name,self.fullname,self.password)  
  
  
from sqlalchemy.orm import (mapper, relationship, sessionmaker)  
#print(User.__table__)   
#print(User.__mapper__)   
  
mapper(User,users_table)  
  
ed_user=User('ed','Ed Jones','edspassword')  
ed_user.password = 'f8s7ccs'  
print(ed_user.fullname)  
print(ed_user.password)  