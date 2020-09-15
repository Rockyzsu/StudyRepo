from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl

app = QApplication([])
view = QWebView()
view.load(QUrl("http://weixin.sogou.com"))
view.show()
app.exec_()


# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtWebKitWidgets import QWebPage
# from lxml import etree
# from lxml.etree import XPathEvalError
#
# #use QtWebkit to get the final webpage
# app = QApplication([])
#
#
# def create_tree(html):
#     '''
#     :param html:HTML或者XML字符串
#     :return:tree树形结构对象
#     '''
#     try:
#         root = etree.HTML(html)
#     except ValueError:
#         root = etree.XML(html)
#     tree = etree.ElementTree(root)
#     return tree
#
# class WebRender(QWebPage):
#     def __init__(self, url):
#         # self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.loadFinished.connect(self.__loadFinished)
#         self.mainFrame().load(QUrl(url))
#         app.exec_()
#
#     def __loadFinished(self, result):
#         self.frame = self.mainFrame()
#         app.quit()
#
# for i in range(1, 67):
#     r = WebRender('http://www.cpnn.com.cn/zdyw/default_{0}.htm'.format(i))
#     html = r.frame.toHtml()
#     tree = create_tree(html)
#     title = tree.xpath("/html/body/div[4]/div[2]/div[1]/div/ul/li[*]/h1/a/text()")
#     print(title)




class QGraphicsWebView(object):

    # def __init__(self, parent: typing.Optional[QtWidgets.QGraphicsItem] = ...) -> None: ...

    # def setRenderHint(self, hint: QtGui.QPainter.RenderHint, enabled: bool = ...) -> None: ...
    # def setRenderHints(self, hints: QtGui.QPainter.RenderHints) -> None: ...
    # def renderHints(self) -> QtGui.QPainter.RenderHints: ...
    # def setTiledBackingStoreFrozen(self, frozen: bool) -> None: ...
    # def isTiledBackingStoreFrozen(self) -> bool: ...

    def foo(self) -> None:
        ...

    def bar(self, number: int=...) -> int:
        return 10 + number

a = QGraphicsWebView()
print(a.bar(20))
