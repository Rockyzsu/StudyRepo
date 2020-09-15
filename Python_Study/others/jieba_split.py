#!urs/bin/env python
#coding:utf-8


import jieba
jieba.enable_parallel(4) # 开启并行分词模式，参数为并行进程数 
jieba.set_dictionary('D:/Python34/Lib/site-packages/jieba/dict_big.txt')


def jieba_split(row):
    seg_list = jieba.cut(row, cut_all = False)  #精确模式
    res = ' '.join(seg_list)
    return res
