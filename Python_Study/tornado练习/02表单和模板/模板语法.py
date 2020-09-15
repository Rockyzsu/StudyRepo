# !/usr/bin/python
#coding:utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.template import Template

# 模板语法
def func01():
    content = Template('<html><body><h1>{{ header }}</h1></body></html>')
    print(content.generate(header="Welcome!"))
    
# 填充表达式
def func02():
    print(Template('{{ 1 + 1 }}').generate())
    print(Template('{{ "scrambled eggs"[-4:] }}').generate())
    print(Template('{{ ", ".join([str(x * x) for x in range(10)]) }}').generate())
    
# 控制流语句
# 控制语句以{%和%}包围，支持if、for、while和try。在这些情况下，语句块以{%开始，并
# 以%}结束。
def func03():
    string = '''
    <html>
        <head>
            <title>{{ title }}</title>
        </head>
        <body>
            <h1>{{ header }}</h1>
            <ul>
                {% set count=0 %}
                {% for book in books %}
                    <li>{{ book }}</li>
                {% end %}
                <p>总共有{{ len(books) }}本书</p>
            </ul>
        </body>
    </html>
    '''
    class BookHandler(tornado.web.RequestHandler):
        def get(self):
            b = Template(string)
            books=['Learning Python', 'Programming Collective Intelligence', 
                   'Restful Web Services']
            content = b.generate(title='Home Page', 
                                 header='Books that are great', 
                                 books=books)
            self.write(content)
            
    app = tornado.web.Application(
        handlers=[(r'/book', BookHandler)],
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
    # 我们也可以在控制语句块中间使用{% set foo='bar' %}来设置变量。我们还有很多可以
    # 在控制语句块中做的事情，但是在大多数情况下，最好使用UI模块来做更复杂的划分。
    
def func04():
    # 在模板中使用函数
    # escape(s)：替换字符串s中的&、<、>为它们对应的HTML字符。
    print(Template('my name is {{ escape("mort&ime>r") }}').generate())
    # url_escape(s)：使用urllib.quote_plus替换字符串s中的字符为URL编码形式。
    print(Template('my name is {{ url_escape("熊大帅") }}').generate())
    # json_encode(val)：将val编码成JSON格式。（这是一个对json库的dumps函数调用）
    print(Template('my name is {{ json_encode("{\'name\':\'熊大帅\'}") }}').generate())
    # squeeze(s)：过滤字符串s，把连续的多个空白字符替换成一个空格。
    print(Template('my name is {{ squeeze("Hello   World   ") }}').generate())
    
    def disemvowel(s):
        return ''.join([x for x in s if x not in 'aeiou'])
    # 在模板中使用一个自己编写的函数也是很简单的：只需要将函数名作为模板的参数传递即可。
    print(Template('my name is {{ d("mortimer") }}').generate(d=disemvowel))
    
    
if __name__ == '__main__':
#     func01()
#     func02()
#     func03()
    func04()