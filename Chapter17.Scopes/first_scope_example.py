#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------
# Usage: python3 scope_example.py
# Description: Scope Example
#-------------------------------


# Global scope
x = 99          # x and func assigned in module: global


def func(y):    # y and z assigned in function: local
    # Local scope
    z = y + x   # x is a global
    return z


res = func(1)   # func in module: return 100

print('res of func is %s' % res)
