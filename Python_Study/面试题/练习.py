#!usr/bin/env python
#coding:utf-8



# 链表
class Node(object):
    def __init__(self, data, p=None):
        self.data = data
        self.next = p
        

class LinkList(object):
    def __init__(self):
        self.head = None
    
    def init(self):
        print('请输入q结束输入：')
        data = input()
        if data is not 'q':
            self.head = Node(data)
        p = self.head
        while data != 'q':
            data = input()
            if data == 'q':
                break
            else:
                p.next = Node(data) # next设置为下一个节点
                p = p.next          # 当前节点下移，设置为下一个节点
        print("输入结束！")
        
    def show(self):
        print("当前序列为：")
        p = self.head
        while p:
            print(p.data)
            p = p.next
            
class A(object):
    count = 1
    
class B(A): pass
class C(A): pass

def foo():
    print(A.count, B.count, C.count)
    B.count = 6
    print(A.count, B.count, C.count)
    A.count = 8
    print(A.count, B.count, C.count)
    
def foo2():
#     return [lambda x: x * i for i in range(4)]
    return (lambda x: x * i for i in range(4))

            
        

if __name__ == '__main__':
#     lk_list = LinkList()
#     lk_list.init()
#     lk_list.show()
    
#     foo()
    for i in foo2():
        print(i(2))