
from lxml import etree
import asyncio
import aiohttp


def create_tree(html):
    root = etree.HTML(html)
    tree = etree.ElementTree(root)
    return tree


async def getPage(url, res_list):
    print(url)
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    # conn = aiohttp.ProxyConnector(proxy="http://127.0.0.1:8087")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            assert resp.status == 200
            res_list.append(await resp.text())


class parseListPage():
    def __init__(self, page_str):
        self.page_str = page_str

    def __enter__(self):
        page_str = self.page_str
        tree = create_tree(page_str)
        # 获取文章链接
        articles = tree.xpath(".//*[@id='article_list']/div[*]/div[1]/h1/span/a/@href")
        articles = ['http://test.csdn.net' + i for i in articles]
        return articles

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


page_url_base = 'http://test.csdn.net/u014595019/article/list/'
page_urls = [page_url_base + str(i+1) for i in range(5)]
loop = asyncio.get_event_loop()
ret_list = []
tasks = [getPage(i, ret_list) for i in page_urls]
loop.run_until_complete(asyncio.wait(tasks))

articles_url = []
for ret in ret_list:
    with parseListPage(ret) as tmp:
        articles_url += tmp
ret_list = []

tasks = [getPage(url, ret_list) for url in articles_url]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()