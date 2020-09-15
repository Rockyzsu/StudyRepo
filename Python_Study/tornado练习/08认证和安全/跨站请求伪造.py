#!urs/bin/env python
#coding:utf-8

import tornado.web
import tornado.httpserver

'''
跨站请求伪造，或XSRF是所有web应用程序面临的一个主要问题。
普遍接受的预防XSRF攻击的方案是让每个用户的cookie都是不确定的值，并且把那个cookie值在
你站点的每个form提交中作为额外的参数包含进来。如果cookie和form提交中的值不匹配，则
请求可能是伪造的。
'''


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.render('xsrf.html')
#         self.write('<html><body><form action="/" method="post">'
#                    '{% module xsrf_form_html() %}'
#                    '<input type="text" name="message"/>'
#                    '<input type="submit" value="Post"/>'
#                    '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")



if __name__ == "__main__":
    settings = {
                'cookie_secret': "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                'login_url': '/login',
                'xsrf_cookies': True
                }
    # 如果设置了xsrf_cookies，tornado web应用程序将会给所有用户设置_xsrf cookie并且
    # 拒绝所有不包含一个正确的_xsrf值的POST、PUT或DELETE请求。如果你打开这个设置，
    # 则必须给所有通过POST请求的form提交添加这个字段，可以使用一个特性的UIModule
    # xsrf_form_html()来做这件事情，这个方法在所有模板中都是可用的。
    application = tornado.web.Application([(r"/", MainHandler), (r"/login", LoginHandler),], 
                                          **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    print('服务器开始运行了！')
    tornado.ioloop.IOLoop.instance().start()
    
'''
如果你调教一个AJAX的POST请求，你也需要在每个请求中给你的JavaScript添加_xsrf值。下面
的例子是在FriendFeed为了AJAX的POST请求使用的一个jQuery函数，可以自动的给所有的请求
添加_xsrf值。
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
        success: function(response) {
        callback(eval("(" + response + ")"));
    }});
};

对于PUT和DELETE请求（除了不使用form编码（form-encoded）参数的POST请求，XSRF token也会
通过一个X-XSRFToken的HTTP头传递。XSRF cookie通常在使用xsrf_form_html会设置，但是在
不使用正规form的纯JavaScript应用中，你可能需要访问self.xsrf_token手动设置（只读这个
属性足够设置cookie了）。
如果你需要自定义每一个处理程序基础的XSRF行为，你可以覆写RequestHandler.check_xsrf_cookie()。
例如，你又一个没有使用cookie验证的API，你可能想禁用XSRF保护，可以通过使check_xsrf_cookie()
不做任何处理。然而，如果你支持基于cookie的非基于cookie的认证，重要哦的是，当前带有cookie
认证的请求究竟什么时候使用XSRF保护。
'''