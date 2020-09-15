#!urs/bin/env python
#coding:utf-8


class User(object):     # 用户
    def __init__(self):
        self.ID = 0
        self.name = ''
        

class Department(object):   # 部门
    def __init__(self): return
        

class IUser(object):
    def Insert(self, user): return
    def GetUser(self, id_): return
    

class SqlserverUser(IUser):
    # 用于访问SQL Server的User
    def Insert(self, user):
        print('在SQL Server中给User表增加一条记录')
        
    def GetUser(self, id_):
        print('在SQL Server中根据ID得到User表一条记录')
        

class AccessUser(IUser):
    # 用于访问Access的User
    def Insert(self, user):
        print('在Access中给User表增加一条记录')
        
    def GetUser(self, id_):
        print('在Access中根据ID得到User表一条记录')
        
################################################################################
class IFactory(object):
    # 定义一个创建访问User表对象的抽象的工厂接口
    def CreateUser(self): return
    def CreateDepartment(self): return  # 增加的接口方法（部门）
    
    
class SqlServerFactory(IFactory):
    # 实例化SqlserverUser
    def CreateUser(self):
        return SqlserverUser()
    
    def CreateDepartment(self):
        return SqlserverDepartment()
    

class AccessFactory(IFactory):
    # 实例化AccessUser
    def CreateUser(self):
        return AccessUser()
    
    def CreateDepartment(self):
        return AccessDepartment()
    
################################################################################
# 增加部门表
class IDepartment(object):
    def Insert(self, department): return
    def GetDepartment(self, id_): return
    
    
class SqlserverDepartment(IDepartment):
    # 用于访问SQL Sever的Department
    def Insert(self, department):
        print('在SQL Server中给Department表增加一条记录')
        
    def GetDepartment(self, id_):
        print('在SQL Server中根据ID得到Department表一条记录')
        

class AccessDepartment(IDepartment):
    # 用于访问SQL Sever的Department
    def Insert(self, department):
        print('在Access中给Department表增加一条记录')
        
    def GetDepartment(self, id_):
        print('在Access中根据ID得到Department表一条记录')
        

def run1():
    user = User()
    su = SqlserverUser()
    su.Insert(user)
    su.GetUser(1)
    
def run2():
    # 工厂方法模式是定义一个用于创建对象的接口，让子类决定实例化哪一个类。
    user = User()
    factory = SqlServerFactory()
    iu = factory.CreateUser()
    iu.Insert(user)
    iu.GetUser(1)
    
def run3():
    user = User()
    dept = Department()
    factory = AccessFactory()
    iu = factory.CreateUser()           # 此时已与具体的数据库访问解除了依赖
    iu.Insert(user)
    iu.GetUser(1)
    
    id_ = factory.CreateDepartment()    # 此时已与具体的数据库访问解除了依赖
    id_.Insert(dept)
    id_.GetDepartment(1)
    
    
# 抽象工厂模式：提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。[DP]
class DataAccess(object):
    db = 'Sqlserver'   # 数据库名称，可替换成Access
#     db = 'Access'

    @staticmethod
    def CreateUser():
        # 由于db的事先设置，所以此处可以根据选择实例化出相应的对象
        result = None
        if DataAccess.db == 'Sqlserver':
            result = SqlserverUser()
        elif DataAccess.db == 'Access':
            result = AccessUser()
        return result
    
    @staticmethod
    def CreateDepartment():
        result = None
        if DataAccess.db == 'Sqlserver':
            result = SqlserverDepartment()
        elif DataAccess.db == 'Access':
            result = AccessDepartment()
        return result
    
# 利用反射技术
class DataAccess2(object):
    db = 'Sqlserver'                 # 数据库名称，可替换成Access
    @staticmethod
    def CreateUser():
        className = DataAccess.db + 'User'
        return eval(className)()
    
    @staticmethod
    def CreateDepartment():
        className = DataAccess2.db + 'Department'
        return eval(className)()
    
# 反射技术+配置文件
import json
def readconfig():
    with open('App.config', 'r') as f:
        lines = f.read()
    return json.loads(lines)

class DataAccess3(object):
    conf = readconfig()
    @staticmethod
    def CreateUser():
        className = DataAccess3.conf['db_name'] + 'User'
        return eval(className)()
    
    @staticmethod
    def CreateDepartment():
        className = DataAccess3.conf['db_name'] + 'Department'
        return eval(className)()

# 所有在用简单工厂的地方，都可以考虑用反射技术来取出switch或if，解除分支判断带来的耦合。
def run4():
    user = User()
    dept = Department()
    iu = DataAccess.CreateUser()
    iu.Insert(user)
    iu.GetUser(1)
    
    id_ = DataAccess.CreateDepartment()
    id_.Insert(dept)
    id_.GetDepartment(1)
    
def run5():
    user = User()
    dept = Department()
    iu = DataAccess3.CreateUser()
    iu.Insert(user)
    iu.GetUser(1)
    
    id_ = DataAccess3.CreateDepartment()
    id_.Insert(dept)
    id_.GetDepartment(1)

        
if __name__ == '__main__':
#     run1()
#     run2()
#     run3()
#     run4()
    run5()
