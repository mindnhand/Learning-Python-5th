#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------
# Usage: python3 5-asserter.py
# Description: assert
#--------------------------------------



def f(x):
    assert x < 0, 'x must be a negative'
    return x ** 2


print(f(-1))
print(f(1))
