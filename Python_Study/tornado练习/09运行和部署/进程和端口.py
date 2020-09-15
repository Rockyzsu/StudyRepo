#!urs/bin/env python
#coding:utf-8


'''
为了充分利用多CPU机器，运行多个python进程是很有必要的。通常，最好是每个CPU运行一个进程。
tornado包含了一个内置的多进程模式来一起启动多个进程：
def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()
这是最简单的方式来启动多进程并让它们共享同样的端口，虽然它有一些局限性。首先，每个子进程
都有自己的IOLoop，所以在fork之前，不接触全局IOLoop实例是很重要的（甚至是间接）。其次，
在这个模型中，很难做到零停机更新。最后，因为所有的进程共享相同的端口，想单独监控它们就
更困难了。
对更加复杂的部署，建议启动独立的进程，并让它们各自监听不同的端口。supervisord的进程组
功能是一个很好的方式来安排这些。当每个进程使用不同的端口，一个外部的负载均衡器例如
HAProxy或nginx通常需要对外向访客提供一个单一的地址。
'''
