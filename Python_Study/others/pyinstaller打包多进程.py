#!urs/bin/env python
#coding:utf-8


import os
import sys
from multiprocessing import Process
import multiprocessing


#===============================================================================
# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen
#pyinstaller打包多进程的先决条件，否则会出现诸如无限个进程的卡死情况。
#===============================================================================

def foo1():
    print('I am foo1')

def foo2():
    print('I am foo2')
    
def foo3():
    print('I am foo3')    

if __name__ == '__main__':
    multiprocessing.freeze_support()    #必须
    a = Process(target = foo1)
    b = Process(target = foo2)
    c = Process(target = foo3)
    a.start()
    b.start()
    c.start()
    
    a.join()    #主进程会等待子进程的完成
    b.join()
    c.join()
    print('主进程已经跑完了')
    