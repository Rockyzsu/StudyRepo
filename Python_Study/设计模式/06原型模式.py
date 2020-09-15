#!urs/bin/env python
#coding:utf-8

# 原型模式：用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。[DP]
# 原型模式其实就是从一个对象再创建另外一个可定制的对象，而且不需要知道任何创建的细节。


import copy


class WorkExperience(object):
    def __init__(self):
        self.WorkDate = ''
        self.Company = ''


class Resume(object):
    def __init__(self, name):
        self.name = name
        self.sex = ''
        self.age = ''
        self.work = WorkExperience()

    def SetPersonalInfo(self, sex, age):
        # 设置个人信息
        self.sex = sex
        self.age = age

    def SetWorkExperience(self, timeArea, company):
        # 设置工作信息
        self.work.WorkDate = timeArea
        self.work.Company = company

    def Display(self):
        # 显示
        print('{0} {1} {2}'.format(self.name, self.sex, self.age))
        print('工作经历：{0} {1}'.format(self.work.WorkDate, self.work.Company))

    def Clone(self):
        return copy.deepcopy(self)

def first():
    a = Resume('大鸟')
    a.SetPersonalInfo('男', '29')
    a.SetWorkExperience('1998-2000', 'XX公司')

    b = a.Clone()
    b.SetWorkExperience('1998-2006', 'YY企业')

    c = a.Clone()
    c.SetPersonalInfo('男', '24')

    a.Display()
    b.Display()
    c.Display()



if __name__ == '__main__':
    first()