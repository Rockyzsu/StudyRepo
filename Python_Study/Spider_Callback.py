# -*- coding: utf-8 -*-
# @Time    : 2017/7/21 11:48
# @Author  : 卧槽
# @Site    : 
# @File    : Spider_Callback.py
# @Software: PyCharm

from requests import Request, Session
from requests.exceptions import ReadTimeout, Timeout

queue = []
session = Session()


class CallBackRequest(Request):

    def __init__(self, url, callback, method='GET', headers=None, timeout=3, proxy=None, params=None, data=None):
        Request.__init__(url, method, headers)
        self.callback = callback
        self.timeout = timeout
        self.proxy = proxy
        self.params = params
        self.data = data


def request(CallBackRequest):
    try:
        if CallBackRequest.proxy:
            proxy = get_proxy()
            if proxy:
                proxies = {
                    'https': proxy,
                    'http' : proxy
                }
                return session.send(CallBackRequest.prepare(),
                                    proxies=proxies,
                                    timeout=CallBackRequest.timeout,
                                    allow_redirects=False)
            pass
        if CallBackRequest.params:
            pass

        if CallBackRequest.data:

            pass

    except Exception as err:
        print(err.args)

    pass

def get_proxy():
    pass