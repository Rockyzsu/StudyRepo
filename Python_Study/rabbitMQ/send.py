import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    '10.10.1.81'))
channel = connection.channel()

string = '''
{
    "key_search": 0,
    "page_node": 1,
    "source_ori": 0,
    "rules": {
        "use": 0,
        "regex": ""
    },
    "id": "1304b89a-15ba-11e7-8ebe-005056c00008",
    "delay": 30,
    "retry": 0,
    "url": "http://www.indaa.com.cn/xwzx/yw_btxw/index_2814.html",
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Cookie": "Hm_lvt_316aaee3e5df3728a87d259326383e14=1492509091; Hm_lpvt_316aaee3e5df3728a87d259326383e14=1492509168",
        "Host": "www.indaa.com.cn",
        "Referer": "http://www.indaa.com.cn/xwzx/yw_btxw/index_2814_71.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
    },
    "params": {},
    "method": "get",
    "date_time": "",
    "login": {
        "login": 0,
        "class": "",
        "check": 0,
        "name": "",
        "pwd": ""
    },
    "proxy": {
        "proxy": 0,
        "type": "http",
        "ip": "",
        "port": 8000,
        "name": "",
        "pwd": ""
    },
    "page": [
        {
            "创建树": {}
        },
        {
            "获得string": {
                "xpath": [
                    1,
                    [
                        "number(substring-after(substring-before(/html/body/div[8]/script, '//共多少页'), 'countPage = '))"
                    ]
                ]
            }
        },
        {
            "最大数字": {
                "min_num": 1,
                "step": 1,
                "format": "http://www.indaa.com.cn/xwzx/yw_btxw/index_2814_{0}.html"
            }
        },
        {
            "手动添加": {
                "url": [
                    "http://www.indaa.com.cn/xwzx/yw_btxw/index_2814.html"
                ]
            }
        },
        {
            "创建树": {}
        },
        {
            "获得string": {
                "xpath": [
                    1,
                    [
                        "/html/body/div[*]/div/h1/a/@href"
                    ]
                ],
                "root": [
                    2,
                    "http://www.indaa.com.cn/xwzx/yw_btxw/"
                ]
            }
        }
    ],
    "xpath": {
        "title": {
            "xpath": [
                ".//*[@id='layer3']/div[1]/div[1]/div[1]/text() | html/body/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/table/tbody/tr[position()<3]/td/text()"
            ],
            "cleaner": "CleanTrim(CleanBase())"
        },
        "publish_date": {
            "xpath": [
                "substring-before(substring-after(.//*[@id='layer3']/div[1]/div[1]/div[2]/text(), '时间：'), '来源')",
                "string(html/body/table/tbody/tr[1]/td[2]/table[1]/tbody/tr[3]/td[1]/span)"
            ],
            "cleaner": "CleanTrim(CleanTime(CleanBase(), '%Y-%m-%d'))"
        },
        "author": {
            "xpath": [
                "substring-after(.//*[@id='layer3']/div[1]/div[1]/div[2]/text(), '作者：')",
                "html/body/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/table/tbody/tr[last()]/td/text()"
            ],
            "cleaner": "CleanSpace(CleanTrim(CleanBase()))"
        },
        "content": {
            "xpath": [
                "string(.//*[@id='ozoom']/founder-content | .//*[@id='layer3']/div[1]/div[2])"
            ],
            "cleaner": "CleanSpace(CleanTrim(CleanBase()))"
        },
        "source": {
            "xpath": [
                "substring-before(substring-after(.//*[@id='layer3']/div[1]/div[1]/div[2]/text(), '来源：'), '作者')"
            ],
            "cleaner": "CleanTrim(CleanBase())"
        }
    },
    "main_key": [],
    "second_key": [],
    "data": {}
}
'''

channel.queue_declare(queue='task_root_queue')

channel.basic_publish(exchange='', routing_key='hello', body=string)
print(" [x] Sent 'Hello World!'")
connection.close()
