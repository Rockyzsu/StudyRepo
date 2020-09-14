# coding:utf-8

'''
@author = super_fazai
@File    : 异步任务时间超时.py
@connect : superonesfazai@gmail.com
'''

from asyncio import get_event_loop
from asyncio import sleep as async_sleep
from async_timeout import timeout as async_timeout
from asyncio import TimeoutError as AsyncTimeoutError

async def do_someing():
    print('do some')
    await async_sleep(3)

    return True

async def main():
    print('main')
    try:
        # 设置超时异常退出
        with async_timeout(timeout=1):
            await do_someing()
    except AsyncTimeoutError:
        print('异步执行task超时!')

    return True

loop = get_event_loop()
res = loop.run_until_complete(main())
print(res)