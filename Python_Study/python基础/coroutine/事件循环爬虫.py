import concurrent.futures
from lxml import etree
import requests

URLS = ['http://www.sgcc.com.cn/xwzx/gsyw/yxfc/index_2.shtml',
        'http://www.sgcc.com.cn/xwzx/gsyw/yxfc/index_3.shtml',
        'http://www.sgcc.com.cn/xwzx/gsyw/yxfc/index_4.shtml',
        'http://www.sgcc.com.cn/xwzx/gsyw/yxfc/index_5.shtml',
        'http://www.sgcc.com.cn/xwzx/gsyw/yxfc/index_6.shtml']
# URLS *= 100


def create_tree(html):
    root = etree.HTML(html)
    tree = etree.ElementTree(root)
    return tree


def load_url(url, d_t='2017-01-07'):
    response = requests.get(url)
    tree = create_tree(response.text)
    date = tree.xpath(".//*[@id='t1']/div[2]/div[1]/ul/li[*]/text()")
    date = [i for idx, i in enumerate(date) if idx % 2]
    date = [i.strip()[1:-1] for i in date]
    length = len(date)
    a = [i for i in date if i >= d_t]
    if length > len(a):
        flag = True
    else:
        flag = False
    return url, response.text, flag


def bar():
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the load operations and mark each future with its URL
        for url in URLS:
            future = executor.submit(load_url, url)
            url, html, flag = future.result()
            print(url)
            if flag:
                break


URLS2 = [
    'http://www.mala.cn/forum-70-2.html',
    'http://www.mala.cn/forum-70-3.html',
    'http://www.mala.cn/forum-70-4.html',
    'http://www.mala.cn/forum-70-5.html',
    'http://www.mala.cn/forum-70-6.html',
    'http://www.mala.cn/forum-70-7.html',
    'http://www.mala.cn/forum-70-8.html',

]


def load_url2(url, num):
    response = requests.get(url, timeout=num)
    return response.text


def bar2():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url2, url, 60): url for url in URLS2}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))


# bar()
bar2()
