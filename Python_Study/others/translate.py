#!urs/bin/env python
#coding:utf-8


'''
本模块用于翻译功能，现在只实现了有道的查询。
接口名为youdao_en_to_chinese，参数为要翻译的英文。
'''

import re
import json
import requests


#不能翻译的，手动加入
CANNOT_TRANSLATE = {
    #like this
    #'Hello' : '你好'
}

headers_youdao = {
    'Host': 'fanyi.youdao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://fanyi.youdao.com/',
    'Content-Length': '116',
    'Cookie': 'YOUDAO_MOBILE_ACCESS_TYPE=1; OUTFOX_SEARCH_USER_ID=-431734973'\
        '@221.237.112.60; JSESSIONID=abcd_P31fPtDr6sV5CKGv; SESSION_FROM_COOKIE='\
        'fanyiweb; _ntes_nnid=af836e2ef887f0b47b723ccdb9a144b7,1478080312945; ___rl'\
        '__test__cookies=1478080543142; OUTFOX_SEARCH_USER_ID_NCOO=1653574079.008794',
    'Connection': 'keep-alive'
}
url_youdao = 'http://fanyi.youdao.com/translate?smartresult=dict&'\
    'smartresult=rule&smartresult=ugc&sessionFrom=null'
pattern = re.compile(r'global\.translatedJson.+?(\{.+\})')


def decorator(func):
    #可能有些不能翻译出来，需要手动添加
    def inner(word):
        result = func(word)
        if 'N/A' == result:
            return CANNOT_TRANSLATE.get(word, 'N/A')
        return result
    return inner

@decorator
def youdao_en_to_chinese(word):
    payload = {'type' : 'AUTO', 'i' : word, 'doctype' : 'utf-8',
               'xmlVersion' : '1.8', 'keyfrom' : 'fanyi.web', 'ue' : 'UTF-8',
               'action' : 'FY_BY_CLICKBUTTON', 'typoResult' : 'true'
    }
    res = requests.post(url_youdao, headers = headers_youdao, data = payload)
    m = pattern.search(res.content.decode('utf-8'))
    if m:
        result = m.group(1)
        result = json.loads(result)
        #提取关键字，基本结构如下
        '{"type":"EN2ZH_CN","errorCode":0,"elapsedTime":0,"translateResult":\
        [[{"src":"Japanese","tgt":"日本"}]], "smartResult":{"type":1,"entries":\
        ["","n. 日本人；日语","adj. 日本（人）的；日语的"]}}'
        return result.get('translateResult')[0][0].get('tgt')
    return 'N/A'

if __name__ == '__main__':
    test = ('Japanese', 'Taiwan Taibei', 'Peking', 'fuck you', 'Tom Hanks', 
            'what are you doing?', 'zhongguo chongqing', 'Alexander'
            )
    for string in test:
        res = youdao_en_to_chinese(string)
        print(res)