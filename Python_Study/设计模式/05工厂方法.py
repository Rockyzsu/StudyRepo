
# 工厂方法模式：定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个
# 类的实例化延迟到其子类。


class LeiFeng(object):
    # 雷锋
    def Sweep(self):
        print("扫地")

    def Wash(self):
        print("洗衣")

    def BuyRice(self):
        print("买米")


class Undergraduate(LeiFeng):
    # 学雷锋的大学生
    def __init__(self):
        print("学雷锋的大学生")


class Volunteer(LeiFeng):
    # 社区志愿者
    def __init__(self):
        print("社区志愿者")


class SimpleFactory(object):
    # 简单雷锋工厂
    @staticmethod
    def CreateLeiFeng(type_):
        if type_ == '学雷锋的大学生':
            return Undergraduate()
        elif type_ == '社区志愿者':
            return Volunteer()


class IFactory(object):
    #抽象雷锋工厂
    @staticmethod
    def CreateLeiFeng():
        return LeiFeng()


class VolunteerFactory(IFactory):
    # 社区志愿者工厂
    @staticmethod
    def CreateLeiFeng():
        return Volunteer()


class UndergraduateFactory(IFactory):
    # 学雷锋的大学生工厂
    @staticmethod
    def CreateLeiFeng():
        return Undergraduate()



def main():
    print('------------简单工厂模式-----------')
    studentA = SimpleFactory.CreateLeiFeng('学雷锋的大学生')
    studentA.BuyRice()
    studentA.Sweep()
    studentA.Wash()

    print('------------工厂方法模式-----------')
    studentB =VolunteerFactory.CreateLeiFeng()
    studentB.BuyRice()
    studentB.Sweep()
    studentB.Wash()

if __name__ == '__main__':
    main()