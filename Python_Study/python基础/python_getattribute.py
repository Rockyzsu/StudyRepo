# !/usr/bin/python
#coding:utf-8




class AA(object):
    @classmethod
    def h(cls):
        cls.domain = cls.__name__


class BB(AA):
    
    
    
    def __getattribute__(self, attribute):
        if 'domain' == attribute:
            return super(BB, self).domain

#     def __getattribute__(self, *args, **kwargs):
#         return AA.__getattribute__(self, *args, **kwargs)


def main():
    AA.h()
    BB.h()
    b = BB()
    print(b.domain)    

if __name__ == '__main__':
    main()
