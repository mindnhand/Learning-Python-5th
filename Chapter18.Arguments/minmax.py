#!/usr/bin/env python3
#encoding=utf-8



#---------------------------------------------------------
# Usage: python3 minmax.py
# Description: minmax function to calculate the minimum and maximum value
#---------------------------------------------------------



def minmax(func, *args):
    res = args[0]
    print('original: %s' % str(args))
    for arg in args[1:]:
        if func(arg, res):
            res = arg
    return res


def lessthan(x, y):                 # can be lambda or eval
    return x < y

def grtrthan(x, y):
    return x > y


min_value = minmax(lessthan, 4, 2, 1, 5, 6, 3)
print('minimum value is %s' % min_value)
print()

max_value = minmax(grtrthan, 4, 2, 1, 4, 6, 3)
print('maximum value is %s' % max_value)
