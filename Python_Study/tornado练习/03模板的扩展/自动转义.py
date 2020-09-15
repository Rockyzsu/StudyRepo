#!urs/bin/env python
#coding:utf-8


'''
tornado默认会自动转义模板中的内容，把标签转换为相应的HTML实体。这样可以防止后端为数据
库的网站被恶意脚本攻击。比如，网站中有一个评论部分，用户可以在这里添加任何他们想说的
文字进行讨论。虽然一些HTML标签在标记和样式冲突时不构成重大威胁（如评论中没有闭<h1>
标签），但<script>标签会允许攻击者加载其他的Javascript文件，打开通向跨站脚本攻击、
XSS或漏洞之门。

在tornado 1.x版本中，模板没有自动转义，所以我们防护措施需要显示地在未过滤的用户上
调用escape()函数。
如果Burt想在footer中使用模板email联系链接，他将不会得到期望的HTML链接：
{% ser mailLink="<a href="mailto:contact@burtsbooks.com">Contact Us</a>" %}
{{ mailLink }}
它在页面源代码中被渲染成如下代码：
&lt;a href=&quot;mailto:contact@burtsbooks.com&quot;&gt;Contact Us&lt;/a&gt;
此时被自动转义了，明显无法让人们联系上Burt。
为了处理这种情况，我们可以禁用自动转义，一种方法是在Application构造函数中传递
autoescape=None，另一种方法是在每页的基础上修改自动转义行为，如下：
{% autoescape None %}
{{ mailLink }}
这些autoescape块不需要结束标签，并且可以设置xhtml_escape来开启自动转义（默认行为），
或None来关闭。
然而，在理想的情况下，我们希望保持自动转义开启以便继续防护我们的网站。因此，我们可以
使用{% raw %}指令来输出不转义的内容。
{% raw mailLink %}
需要特别注意的是，当我们使用诸如tornado的linkify()和xsrf_form_html()函数时，自动转义
的设置被改变了。所以如果希望在前面代码的footer中使用linkify()来包含链接，那么可以使用
一个{% raw %}块。
'''

