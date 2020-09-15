# !/usr/bin/python
#coding:utf-8



#设计模式
#第一章 简单工厂模式

'''
UML类图

                ----------------------            --------------------------
                |        运算类             |            |        简单工厂类             |
                |+NumberA: double    |            |                        | 
                |+NumberB: double    |<———————————|+createOperate(): 运算类 |
                |+GetResult(): double|            --------------------------
                ----------------------
                                                   △
                          |
          .——————————————————————————————————————————————————————.
          |                |                |                    |
-----------------------    |    -----------------------          |
|        加法类               |    |    |        乘法类               |          |
|+GetResult(): double |    |    |+GetResult(): double |          |
-----------------------    |    -----------------------          |
                -----------------------                -----------------------
                |        减法类               |                |        除法类               |
                |+GetResult(): double |                |+GetResult(): double |
                -----------------------                -----------------------

'''


class Operation(object):
    def __init__(self, number_a = 0, number_b = 0):
        self.number_a = number_a
        self.number_b = number_b
        
    def getResult(self):
        return 


class Add(Operation):
    def getResult(self):
        return self.number_a + self.number_b


class Sub(Operation):
    def getResult(self):
        return self.number_a - self.number_b


class Mul(Operation):
    def getResult(self):
        return self.number_a * self.number_b


class Div(Operation):
    def getResult(self):
        if 0 != self.number_b:
            return self.number_a / self.number_b
        else:
            raise ZeroDivisionError('除数不能为0！')


class Factory(object):
    #工厂生产
    @staticmethod
    def product(operate):
        if '+' == operate:
            return Add()
        elif '-' == operate:
            return Sub()
        elif '*' == operate:
            return Mul()
        elif '/' == operate:
            return Div()


class Factory_2(object):
    #另一种实现
    Items = {'+' : Add, '-' : Sub, '*' : Mul, '/' : Div}
    def __new__(cls, operate):
        return Factory_2.Items.get(operate)()

def main():
#     obj = Factory.product('+')
    obj = Factory_2('+')
    obj.number_a = 10
    obj.number_b = 20
    print(obj.getResult())
    
     
if __name__ == '__main__':
    main()
