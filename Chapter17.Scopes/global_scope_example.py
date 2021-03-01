#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 global_scope_example.py
# Description: global in function definition
#-------------------------------------------


x = 88          # Global x

print('before func, x = %s' % x)

def func():
    global x
    x = 99      # Global x: outside func, modify the x in global

func()

print('after func, x = %s' % x)     # print 99
