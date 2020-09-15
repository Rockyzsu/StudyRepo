#!urs/bin/env python
#coding:utf-8


# 模板方法模式：定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类
# 可以不改变一个算法的结构即可重定义该算法的某些特定步骤。

'''
UML类图
-------------------
|    TestPaper    |        实现了一个模板方法，定义了算法的骨架，
|+TemplateMethod()|--------具体子类将重定义Operation以实现一个
|+Operation1()    |        算法步骤。
|+Operation2()    |
-------------------
               △
        |
--------------------
|    TestPaper*    |        实现Operation以完成算法中与
|                  |--------特定子类相关的算法步骤。
|+Operation1()     |        
|+Operation2()     |
--------------------
'''

import abc

class TestPaper(metaclass=abc.ABCMeta):
    def TestQuestion1(self):
        print("明十三陵在什么地方？ a. 北京 b. 河北 c. 山东 d. 河南")
        print('答案：%s' % self.Answer1())
        
    def TestQuestion2(self):
        print('晚晴四大名臣中没有谁？ a. 张之洞 b. 左宗棠 c. 李鸿章 d. 刘坤一')
        print('答案：%s' % self.Answer2())
        
    def TestQuestion3(self):
        print('中日甲午战争后，哪一项不是中国赔偿项目？ a. 赔款2亿元白银 \
            b. 割让台湾 c. 割让山东半岛 d. 割让辽沈半岛'
            )
        print('答案：%s' % self.Answer3())
        
    @abc.abstractmethod
    def Answer1(self): return
    @abc.abstractmethod
    def Answer2(self): return
    @abc.abstractmethod
    def Answer3(self): return
    

class TestPaperA(TestPaper):
    # 学生小明抄的试卷
    def Answer1(self): return 'a'
    
    def Answer2(self): return 'c'
    
    def Answer3(self): return 'd'
    
    
class TestPaperB(TestPaper):
    # 学生韩梅梅抄的试卷
    def Answer1(self): return 'a'
    
    def Answer2(self): return 'd'

    def Answer3(self): return 'c'


def run():
    print('小明抄的试卷以及答案：')
    a = TestPaperA()
    a.TestQuestion1()
    a.TestQuestion2()
    a.TestQuestion3()
    
    print('韩梅梅抄的试卷以及答案：')
    b = TestPaperB()
    b.TestQuestion1()
    b.TestQuestion2()
    b.TestQuestion3()
    

if __name__ == '__main__':
    run()