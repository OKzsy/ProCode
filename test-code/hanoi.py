#!/usr/bin/env python
# -*- coding:utf-8 -*-




count = 0


def move(source, target):
    global count
    print(source, "==>", target)

    count += 1


def hanoi(n, source, temp, target):
    if n == 1:
        move(source, target)
    else:
        hanoi(n - 1, source, target, temp)
        move(source, target)
        hanoi(n - 1, temp, source, target)


n = int(input("输入盘子个数： "))
print("移动", n, "个盘子的步骤是：")
hanoi(n, "A", "B", "C")
print(count)
