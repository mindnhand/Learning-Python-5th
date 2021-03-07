#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 timer0.py
# Description: the usage of time module
#---------------------------------------------




import time

def timer(func, *args):
    start = time.time()
    for i in range(1000):
        func(*args)
    return time.time() - start


t1 = timer(pow, 2, 1000)
t2 = timer(str.upper, 'spam')


print('2 ** 1000 comsume %s seconds' % t1)
print('str.upper consume %s seconds' % t2)
