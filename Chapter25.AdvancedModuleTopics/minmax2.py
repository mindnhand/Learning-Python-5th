#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 minmax2.py
# Description: __name__ test
#----------------------------------------------


print('I am: ', __name__)


def minmax(test, *args):
    res = args[0]
    for arg in args[1:]:
        if test(arg, res):
            res = arg
    return res


def lessthan(x, y):
    return x < y

def morethan(x ,y):
    return x > y


if __name__ == '__main__':
    print(minmax(lessthan, 4, 2, 1, 5, 6, 3))           # self-test code
    print(minmax(morethan, 4, 2, 1, 5, 6, 3))


'''
命令行执行结果如下所示：
[root@localhost Chapter25.AdvancedModuleTopics]# python3 minmax2.py
I am:  __main__
1
6
交互式执行结果如下所示：
In [98]: import minmax2
I am:  minmax2

In [99]: minmax2.minmax(minmax2.lessthan, 's', 'p', 'a', '[' )
    ...: 
    ...: 
    ...: 
Out[99]: '['

In [100]: minmax2.minmax(minmax2.lessthan, 's', 'p', 'a', 'a')
     ...: 
Out[100]: 'a'

In [101]: 
'''
