#!urs/bin/env python
#coding:utf-8

def foo():
    # 杨辉三角
    l = [1]
    while True:
        if 1 == len(l):
            yield l
            l.append(1)
        else:
            yield l
            new = [l.pop(0)]                # 直接先取第一个元素到新列表中
            for idx, i in enumerate(l):
                new.append(i + l[idx - 1])  # 当前值加上前一个值
            new.append(1)                   # 最后追加一个1
            l = new


if __name__ == '__main__':
    n = 0
    for i in foo():
        n += 1
        if n > 10: break
        print(i)