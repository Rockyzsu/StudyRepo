#!urs/bin/env python
#coding:utf-8


'''
tornado中，你可以通过在应用程序中指定特殊的static_path来提供静态文件服务：
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
], **settings)
这些设置将自动把所有以/staic/开头的请求从static目录进行提供。e.g：http://localhost:
8888/static/foo.png将会通过指定的static目录提供foo.png文件。我们也自动的会从static
目录提供/robots.txt和/favicon.ico（尽管他们并没有以/static/前缀开始）。
在上面的设置中，我们明确的配置Tornado 提供 apple-touch-icon.png 文件从
StaticFileHandler 根下，虽然文件在static文件目录中。(正则表达式捕获组必须告诉 
StaticFileHandler 请求的文件名；调用捕获组 把文件名作为方法的参数传递给处理程序。)
你可以做同样的事情 。e.g：从网站的根提供 sitemap.xml 文件. 当然, 你也可以通过在你的
HTML中使用 <link /> 标签来避免伪造根目录的 apple-touch-icon.png。

为了改善性能，通常情况下，让浏览器主动缓存静态资源是个好主意，这样浏览器就不会发送不
必要的可能在渲染页面时阻塞的If-Modified-Since或Etag请求了。tornado使用静态内容版本
来支持此项功能。
为了使用这些功能，在你的模板中使用static_url方法而不是直接在你的HTML中输入静态文件的
URL：
<html>
   <head>
      <title>FriendFeed - {{ _("Home") }}</title>
   </head>
   <body>
     <div><img src="{{ static_url("images/logo.png") }}"/></div>
   </body>
 </html>
static_url()函数将把相对路径翻译成一个URI类似于/static/images/logo.png?v=aae54。
其中v参数是logo.png内容的哈希，并且它的存在使得tornado向用户的浏览器发送缓存头，这将
使浏览器无限期缓存内容。
因为参数v是基于文件内容的，如果你更新一个文件并重启服务，它将发送一个新的v值，所以用户
的浏览器将会自动的拉去新的文件。如果文件的内容没有改变，浏览器将会继续使用本地缓存的副
本，而不会从服务器检查更新，显著地提高了渲染性能。
在生产中，你可能想提供静态文件通过一个更优的静态服务器，比如nginx。你可以配置任何web
服务器通过识别static_url()提供的版本标签并设置相应的缓存头。下面是我们在FriendFeed
使用的nginx相关配置的一部分：
location /static/ {
    root /var/friendfeed/static;
    if ($query_string) {
        expires max;
    }
 }

'''

if __name__ == '__main__':
    pass