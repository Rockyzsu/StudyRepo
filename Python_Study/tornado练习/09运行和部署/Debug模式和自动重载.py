#!urs/bin/env python
#coding:utf-8


'''
如果传递 debug=True 配置给 Application 的构造函数, 应用程序将会 运行在debug/开发模式.
在这个模式下, 为了方便于开发的一些功能将被启用( 每一个也可以作为独立的标签使用; 如果
它们都被专门指定, 那它们都将获得 独立的优先级):
•autoreload=True: 应用程序将会观察它的源文件是否改变, 并且当任何 文件改变的时候便
重载它自己. 这减少了在开发中需要手动重启服务的需求. 然而, 在debug模式下, 某些错误
(例如import的时候有语法错误)会导致服务 关闭, 并且无法自动恢复.
•compiled_template_cache=False: 模板将不会被缓存.
•static_hash_cache=False: 静态文件哈希 (被 static_url 函数 使用) 将不会被缓存
•serve_traceback=True: 当一个异常在 RequestHandler 中没有捕获, 将会生成一个包含
调用栈信息的错误页.
自动重载(autoreload)模式和 HTTPServer 的多进程模式不兼容. 你不能给 HTTPServer.start 
传递1以外的参数(或者调用 tornado.process.fork_processes) 当你使用自动重载模式的时候.
debug模式的自动重载功能可作为一个独立的模块位于 tornado.autoreload. 以下两者可以结合
使用, 在语法错误之时提供额外的健壮性: 设置 autoreload=True 可以在app运行时检测文件
修改, 还有启动 python -m tornado.autoreload myserver.py 来捕获任意语法错误或者 其他
的启动时错误.
重载会丢失任何Python解释器命令行参数(e.g. -u). 因为它使用 sys.executable 和 sys.argv
重新执行Python. 此外, 修改这些变量 将造成重载错误.
在一些平台(包括Windows 和Mac OSX 10.6之前), 进程不能被”原地”更新, 所以当检测到代码更新,
旧服务就会退出然后启动一个新服务. 这已经被公知 来混淆一些IDE.
'''