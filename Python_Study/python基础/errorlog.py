#!urs/bin/env python
#coding:utf-8


import traceback

if __name__ == '__main__':
    try:
        raise
    except:
        with open('error.log', 'w') as f:
            traceback.print_exc(file = f)