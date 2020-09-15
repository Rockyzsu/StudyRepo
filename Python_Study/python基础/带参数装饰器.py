# !/usr/bin/python
#coding:utf-8



def trace(log_level):
    def impl_f(func):
        print(log_level, 'Implementing function: "{}"'.format(func.__name__))
        return func
    return impl_f


@trace('[INFO]')
def print_msg(msg):
    print(msg)
#等价于
# temp = trace('[INFO]')
# print_msg = temp(print_msg)

def main():
    print_msg('......')

if __name__ == '__main__':
    main()
