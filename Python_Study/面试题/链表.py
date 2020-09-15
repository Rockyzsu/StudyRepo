#!usr/bin/env python
#coding:utf-8

class Node(object):
    def __init__(self,data, p=0):
        self.data = data
        self.next = p
        
        
class LinkList(object):
    def __init__(self):
        self.head = 0

    def initlist(self):
        print("input numbers here.'!' to quit")

        data=input()
        if data is not '-1':
            self.head=Node(int(data))
        p=self.head
        while data != '-1':
            data=input()
            if data == '-1':
                break
            else:
                p.next=Node(int(data))
                p=p.next

        print("输入结束！")
        print("输入结束,当前序列为:")
        p=self.head
        while p!=0:
            print(p.data)
            p=p.next

    def getlength(self):
        p = self.head
        length = 0
        while p!=0:
            length+=1
            p = p.next
        print("当前链表的长度为%d="%length)

    def is_empty(self):
        if self.getlength() ==0:
            return True
        else:
            return False

    def clear(self):
        self.head = 0

    def append(self,item):
        q = Node(item)
        if self.head ==0:
            self.head = q
        else:
            p = self.head
            while p.next!=0:
                p = p.next
                p.next = q
            print("在链表尾部插入数据后，链表为:")
            p=self.head
            while p!=0:
                print(p.data)
                p=p.next

    def getitem(self,index):
        if self.is_empty():
            print ('Linklist is empty.')
            return
        j = 0
        p = self.head

        while p.next!=0 and j <index:
            p = p.next
            j+=1

        if j ==index:
            #return p.data
            print("在链表的%d位置上的数值是"%(p.data))
        else:
            print ('target is not exist!')

    def insert(self,index,item):
        if self.is_empty() or index<0 or index >self.getlength():
            print ('Linklist is empty.')
            return
        p=self.head
        if index ==0:
            q = Node(item)
            q.next=self.head
            self.head=q
        else:
            p = self.head
            post  = self.head
            j = 0
            while p.next!=0 and j<index:
                post = p
                p = p.next
                j+=1

            if index ==j:
                q = Node(item,p)
                post.next = q
                q.next = p
        p=self.head
        print("插入某个值后的链表")
        while p!=0:
            print(p.data)
            p=p.next

    def delete(self,index):
        if self.is_empty() or index<0 or index >self.getlength():
            print ('Linklist is empty.')
            return
        p=self.head
        if index ==0:
            q = self.head

            self.head = q.next
            p=self.head
        else:
            p = self.head
            post  = self.head
            j = 0
            while p.next!=0 and j<index:
                post = p
                p = p.next
                j+=1

            if index ==j:
                post.next = p.next
        print("删除某个节点后的链表:")
        p=self.head
        while p!=0:
            print(p.data)
            p=p.next
            
    def index(self,value):
        if self.is_empty():
            print ('Linklist is empty.')
            return

        p = self.head
        i = 0
        while p.next!=0 and not p.data ==value:
            p = p.next
            i+=1
        
        if p.data == value:
            #return i
            print("要找的值在链表中的第%d位,"%(i+1))
        else:
            #return -1
            print("没有此值!")

    def rever(self):
        self.initlist()
#         p=self.head
        nex=self.head.next
        pre=Node(0)
        while self.head.next!=0:
            nex=self.head.next
            self.head.next=pre
            pre=self.head
            self.head=nex
        self.head.next=pre
        pre=self.head1

        print("逆序输出节点:")
        #此处的0是链表结尾处代表结束的，而pre链表的整个序列是2,1,0-->这个0代表整数0
        while pre.next!=0:
            print(pre.data)
            pre=pre.next



if __name__=="__main__":
    l = LinkList()
    l.initlist()
    l.rever()
    l.getlength()
    l.getitem(0)
    l.delete(0)
    l.insert(0,1)
    l.index(2)
    l.getitem(0)
    l.append(1)