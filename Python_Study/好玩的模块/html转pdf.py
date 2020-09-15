# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 16:57
# @Author  : 卧槽
# @Site    : 
# @File    : html转pdf.py
# @Software: PyCharm
import pdfkit

config=pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
pdfkit.from_url('http://www.jb51.net/article/85455.htm', 'out.pdf', configuration=config)
