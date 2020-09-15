
# 插入排序
'''
插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据，
算法适用于少量数据的排序，时间复杂度为O(n^2)，是稳定的排序方法。插入算法把要排序的数组分成两部分：第
一部分包含了这个数组的所有元素，但将最后一个元素除外（让数组多一个空间才有插入的位置），而第二部分就
只包含这一个元素（即待插入元素）。在第一部分排序完成后，再将这个最后元素插入到已排好序的第一部分中。
'''
def insert_sort(lists):
    # 插入排序
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            print(lists)
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            else:
                break
            j -= 1
    print(lists)

def bubble_sort(lists):
    # 冒泡排序
    count = len(lists)
    for i in range(count):
        for j in range(i + 1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    print(lists)


def main():
    lists = [23, -23, -67, 999, 1, 0, 23.22, -234]
    # insert_sort(lists)
    bubble_sort(lists)


if __name__ == '__main__':
    main()