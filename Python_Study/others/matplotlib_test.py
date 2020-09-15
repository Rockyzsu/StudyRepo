#!urs/bin/env python
#coding:utf-8

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from numpy  import array
import numpy as np
import matplotlib.pyplot as plt  


def foo():
    fig = plt.figure()  
    ax = fig.add_subplot(111)  
    DataX =[1,2,3,4,5,6,7]  
    DataY =[7,6,5,4,3,2,1]  
    ax.scatter(DataX,DataY,15.0*array(DataX),15.0*array(DataY))  
    plt.show()  
    
def bar():
    x = np.linspace(0, 10, 1000)
    y = np.sin(x)
    z = np.cos(x**2)
    
    plt.figure(figsize=(8,4))
    plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
    plt.plot(x,z,"b--",label="$cos(x^2)$")
    plt.xlabel("Time(s)")
    plt.ylabel("Volt")
    plt.title("PyPlot First Example")
    plt.ylim(-1.2,1.2)
    plt.legend()
    plt.show()


def bin():
    labels = 'A', 'B', 'C', 'D'
    fracs = [15, 30.55, 44.44, 10]
    explode = [0, 0.1, 0, 0]  # 0.1 凸出这部分，
    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    # autopct ，show percet
    plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6

            )
    '''
    labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    shadow，饼是否有阴影
    startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    pctdistance，百分比的text离圆心的距离
    patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    '''
    plt.show()


def zhu():
    data = [5, 20, 15, 25, 10]
    plt.bar(range(len(data)), data)
    plt.show()


def threeD():
    fig = figure()
    ax = Axes3D(fig)
    X = np.arange(-4, 4, 0.25)
    Y = np.arange(-4, 4, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot')
    show()


def map():
    def f(x, y): return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)

    n = 256
    x = np.linspace(-3, 3, n)
    y = np.linspace(-3, 3, n)
    X, Y = np.meshgrid(x, y)

    contourf(X, Y, f(X, Y), 8, alpha=.75, cmap='jet')
    C = contour(X, Y, f(X, Y), 8, colors='black', linewidth=.5)
    show()


def point():
    n = 1024
    X = np.random.normal(0, 1, n)
    Y = np.random.normal(0, 1, n)

    scatter(X, Y)
    show()


def huidu():
    def f(x, y): return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)

    n = 10
    x = np.linspace(-3, 3, 4 * n)
    y = np.linspace(-3, 3, 3 * n)
    X, Y = np.meshgrid(x, y)
    imshow(f(X, Y)), show()


if __name__ == '__main__':
#     foo()
#     bar()
#     bin()
#     zhu()
#     threeD()
#     map()
    point()
    # huidu()

