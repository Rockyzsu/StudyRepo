#!usr/bin/env python
#coding:utf-8

from tqdm import tqdm


class ProcessBar(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = object.__new__(cls)
        return cls._inst
    
    def __init__(self, total, filename = ''):
        self.processbar = tqdm(total=total, unit_scale = True, 
                               desc = filename, unit = '',
                               )
    
    def update(self, already):
        self.processbar.update(already)   
        
    def close(self):
        self.processbar.close()
        
        
if __name__ == '__main__':
    from time import sleep
    a = ProcessBar(1000000000, 'processbar')
    for i in range(100000):
        sleep(0.01)
        a.update(100000)
     
    
    
    
