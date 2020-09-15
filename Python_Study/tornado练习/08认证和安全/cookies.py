#!urs/bin/env python
#coding:utf-8


'''
tornado的安全cookie保证完整性但是不保证机密性，也就是说，cookie不能被修改，但是
它的内容对用户是可见的。秘钥cookie_secret是一个对称的key，而且必须保密——任何获得
这个key的人都可以伪造出自己前面的cookie。
默认情况下，tornado的安全cookie过期时间是30天，可以给set_secure_cookie使用expires_days
关键字参数，同时给get_secure_cookie设置max_age_days参数也可以达到效果。
tornado也支持多签名秘钥，使签名秘钥轮换，然后cookie_secret必须是一个整数key版本作为
key，以相对应的秘钥作为值的字典。当前使用的签名键必须是应用设置中key_version的集合。
不过字典中的其他key都允许做cookie签名，如果当前key版本在cookie集合中，为了实现cookie
更新，可以通过get_secure_cookie_key_version查询当前key版本。
'''


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("mycookie"):
#             self.set_cookie("mycookie", "myvalue")
            self.set_secure_cookie("mycookie", "myvalue", expires_days=1)    # 安全方式
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    # 使用安全cookie的时候必须在创建应用时指定cookie_secret的秘钥
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)],
                                  cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
                                  )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()


