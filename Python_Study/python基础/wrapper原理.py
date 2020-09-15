# !/usr/bin/python
#coding:utf-8



import functools
import sys
debug_log = sys.stdout


def trace(func):
    if debug_log:
#         @functools.wraps(func)
        def callf(*args, **kwargs):
            '''A warpper function.'''
            debug_log.write('Calling function: {}\n'.format(func.__name__))
            res = func(*args, **kwargs)
            debug_log.write('Return value: {}\n'.format(res))
            return res
        
        #相同调用
#         _temp = functools.wraps(func)
#         callf = _temp(callf)

        #展开wraps
#         _temp = functools.partial(functools.update_wrapper,
#                                   wrapped = func,
#                                   assigned = functools.WRAPPER_ASSIGNMENTS,
#                                   updated = functools.WRAPPER_UPDATES)
#         callf = _temp(callf)

        #展开partial
        callf = functools.update_wrapper(callf,
                                  wrapped = func,
                                  assigned = functools.WRAPPER_ASSIGNMENTS,
                                  updated = functools.WRAPPER_UPDATES)
        
        return callf
    else:
        return func

@trace
def square(x):
    '''Calculate the square of the given number.'''
    return x * x


def main():
    print(square(3))
    print(square.__doc__)
    print(square.__name__)

if __name__ == '__main__':
    main()
