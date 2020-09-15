#!urs/bin/env python
#coding:utf-8


# 状态模式：当一个对象的内在状态改变时允许改变其行为，这个对象看起来像是改了了其类。[DP]
# 状态模式主要解决的是当控制一个对象状态转换的条件表达式过于复杂时的情况。把状态的判断
# 逻辑转移到表示不同状态的一系列类当中，可以把复杂的判断逻辑简化。当然，如果这个状态
# 判断很简单，那就没必要用状态模式了。


from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    # 抽象状态
    @abstractmethod
    def WriteProgram(self, w): return
    

class ForenoonState(State):
    # 上午工作状态类
    def WriteProgram(self, w):
        if w.Hour < 12:
            print('当前时间：{0}点 上午工作，精神百倍'.format(w.Hour))
        else:
            w.SetState(NoonState()) # 超过12点，则转入中午工作状态
            w.WriteProgram()
            
            
class NoonState(State):
    # 中午工作状态
    def WriteProgram(self, w):
        if w.Hour < 13:
            print('当前时间：{0}点 饿了，午饭；犯困，午休。'.format(w.Hour))
        else:
            w.SetState(AfternoonState()) # 超过13点，则转入下午工作状态
            w.WriteProgram()
            

class AfternoonState(State):
    # 下午和傍晚工作状态类
    def WriteProgram(self, w):
        if w.Hour < 17:
            print('当前时间：{0}点 下午状态还不错，继续努力'.format(w.Hour))
        else:
            w.SetState(EveningState()) # 超过17点，则转入傍晚工作状态
            w.WriteProgram()
            
            
class EveningState(State):
    # 晚间工作状态
    def WriteProgram(self, w):
        if w.TaskFinished:
            w.SetState(RestState()) # 如果完成任务，则转入下班状态
            w.WriteProgram()
        else:
            if w.Hour < 21:
                print('当前时间：{0}点 加班哦，疲累之极'.format(w.Hour))
            else:
                w.SetState(SleepingState()) # 超过21点，则转入睡眠工作状态
                w.WriteProgram()
    
class SleepingState(State):
    # 睡眠状态
    def WriteProgram(self, w):
        print('当前时间：{0}点 不行了，睡着了。'.format(w.Hour))
                 

class RestState(State):
    # 下班休息状态
    def WriteProgram(self, w):
        print('当前时间：{0}点下班回家了'.format(w.Hour))  
        
        
class Work(object):
    # 工作类，这时没有过长的分支判断语句
    def __init__(self):
        self.current = ForenoonState()  # 工作初始化为上午工作状态，即上午9点开始上班
        self.Hour = 0                   # 钟点属性，状态转换的依据
        self.TaskFinished = False       # 任务完成属性，是否能下班的依据
        
    def SetState(self, s):
        self.current = s
        
    def WriteProgram(self):
        self.current.WriteProgram(self)
    
    
# 此时的代码，如果要加上“员工必须在20点之间离开公司”，我们只要增加一个“强制下班状态”，
# 并改动一下“傍晚工作状态”类的判断就可以了。而这是不影响其他状态的代码的。    

def main():
    # 紧急项目
    em_projects = Work()
    em_projects.Hour = 9
    em_projects.WriteProgram()
    em_projects.Hour = 10
    em_projects.WriteProgram()
    em_projects.Hour = 12
    em_projects.WriteProgram()
    em_projects.Hour = 13
    em_projects.WriteProgram()
    em_projects.Hour = 14
    em_projects.WriteProgram()
    em_projects.Hour = 17
    em_projects.WriteProgram()
    
    em_projects.TaskFinished = True    
#     em_projects.TaskFinished = False
    em_projects.Hour = 19
    em_projects.WriteProgram()
    em_projects.Hour = 22
    em_projects.WriteProgram()
       
    

if __name__ == '__main__':
    main()
    