#!usr/bin/env python
#coding:utf-8


'''
有两个序列a,b，大小都为n,序列元素的值任意整形数，无序；
要求：通过交换a,b中的元素，使[序列a元素的和]与[序列b元素的和]之间的差最小。
方案：
1. 将两序列合并为一个序列，并排序，为序列Source
2. 拿出最大元素Big，次大的元素Small
3. 在余下的序列S[:-2]进行平分，得到序列max，min
4. 将Small加到max序列，将Big加到min序列，重新计算新序列和，和大的为max，小的为min。
'''

def mean(sorted_list):
    if not sorted_list:
        return [], []
    big = sorted_list[-1]
    small = sorted_list[-2]
    big_list, small_list = mean(sorted_list[:-2])
    big_list.append(small)
    small_list.append(big)
    big_list_sum = sum(big_list)
    small_list_sum = sum(small_list)
    if big_list_sum > small_list_sum:
        return big_list,small_list
    return small_list,big_list

tests = [
         [1,2,3,4,5,6,700,800],
         [10001,10000,100,90,50,1],
         list(range(1, 11)),
         [12312, 12311, 232, 210,30, 29, 3, 2, 1, 1]
]
for l in tests:
    l.sort()
    print()
    print("Source List:\t", l)
    l1,l2 = mean(l)
    print("Result List:\t", l1, l2)
    print("Distance:\t", abs(sum(l1)-sum(l2)))
    print("-*" * 40)
