---
layout: post
title: HTTrack - 克隆任意网站
---

HTTrack可以克隆指定网站－把整个网站下载到本地。

可以用在离线浏览上，也可以用来收集信息（甚至有网站使用隐藏的密码文件）。

一些仿真度极高的伪网站（为了骗取用户密码），也是使用类似工具做的。

Kali Linux默认安装了HTTrack。

HTTrack帮助：
```shell
# httrack --help
```
使用示例：
```shell
# httrack http://topspeedsnail.com -O /tmp/topspeedsnail
```
上面命令克隆了本网站。