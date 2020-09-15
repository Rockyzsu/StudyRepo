#encoding=utf-8
import jieba
jieba.set_dictionary('E:/Python35/Lib/site-packages/jieba/big_dict.txt')

seg_list = jieba.cut("我来到北京清华大学",cut_all=True)
print("Full Mode:", "/ ".join(seg_list)) #全模式
 
seg_list = jieba.cut("我来到北京清华大学",cut_all=False)
print("Default Mode:", "/ ".join(seg_list)) #精确模式
 
seg_list = jieba.cut("他来到了网易杭研大厦") #默认是精确模式
print(", ".join(seg_list))
 
seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") #搜索引擎模式
print(", ".join(seg_list))



content = """
2016年7月24日夜，攻克共匪成都市武侯区纺织高等专科学校财务处综合信息门户。
2016年7月6日夜，攻克共匪大连社会组织网。
今天我很高兴，因为我捡到了200万。
2016年7月9日夜，攻克共匪山东荣成市网上中介超市。 
"""


seg_list = jieba.cut(content,cut_all=False)
set_mode = {'成都市', '重庆市', '上海市', '武侯区'}
seg_list = filter(lambda x: x in set_mode, seg_list)
print("Default Mode:", "-".join(seg_list))
# print(seg_list)
