#!urs/bin/env python
#coding:utf-8


'''
UI模块是封装模板中包含的标记、样式以及行为的可复用组件。它所定义的元素通常用
于多个模板交叉复用或在同一个模板中重复使用。模块本身是一个继承自 Tornado的
UIModule类的简单  Python类，并定义了一个render方法。当一个模板使用{%module
Foo(...) %}标签引用一个模块时，Tornado的模板引擎调用模块的render方法，然
后返回一个字符串来替换模板中的模块标签。UI模块也可以在渲染后的页面中嵌入自己
的 JavaScript和  CSS文件，或指定额外包含的 JavaScript或  CSS文件。你可以定义
可选的embedded_javascript、embedded_css、javascript_files和css_files
方法来实现这一方法。
'''

'''
很多时候，一个非常有用的做法是让模块指向一个模板文件而不是在模块类中直接渲染
字符串。这些模板的标记看起来就像我们已经看到过的作为整体的模板。
UI模块的一个常见应用是迭代数据库或  API查询中获得的结果，为每个独立项目的数
据渲染相同的标记。比如，Burt想在  Burt's Book里创建一个推荐阅读部分，他已经创
建了一个名为 recommended.html的模板，其代码如下所示。就像前面看到的那样，我
们将使用{% module Book(book) %}标签调用模块。
UI模块查找的规则为“BookModule”，只取“Module”的前部分。
'''

# 嵌入JavaScript和CSS
'''
见hello_modules
tornado允许使用embedded_css和embedded_javascript方法嵌入其他的CSS和JavaScript文件。

当一个模块需要额外的库而应用的其他地方不是必需的时候，这种方式非常有用。比如，
你有一个使用 JQuery UI库的模块（而在应用的其他地方都不会被使用），你可以只在
这个样本模块中加载 jquery-ui.min.js文件，减少那些不需要它的页面的加载时间。
因为模块的内嵌 JavaScript和内嵌 HTML函数的目标都是紧邻</body>标签，
html_body()、javascript_files()和 embedded_javascript()都会将内容渲染后插到页面底
部，那么它们出现的顺序正好是你指定它们的顺序的倒序。
'''
import tornado
class SampleModule(tornado.web.UIModule):
    def render(self, sample):
        return self.render_string(
        "modules/sample.html",
        sample=sample
        )
    def html_body(self):
        return "<div class=\"addition\"><p>html_body()</p></div>"
    def embedded_javascript(self):
        return "document.write(\"<p>embedded_javascript()</p>\")"
    def embedded_css(self):
        return ".addition {color: #A1CAF1}"
    def css_files(self):
        return "/static/css/sample.css"
    def javascript_files(self):
        return "/static/js/sample.js"
'''
html_body()最先被编写，它紧挨着出现在</body>标签的上面。embedded_javascript()
接着被渲染，最后是 javascript_files()。
需要小心的是，不能包括一个需要其他地方东西的方法（比如依赖其他文件的
JavaScript函数），因为此时它们可能会按照和你期望不同的顺序进行渲染。
'''

if __name__ == '__main__':
    pass