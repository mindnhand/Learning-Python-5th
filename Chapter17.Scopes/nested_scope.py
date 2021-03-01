#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------
# Usage: python3 nested_scope.py
# Description: enclosed scope
#-------------------------------



x = 99                  # Global scope x


def f1():
    x = 88              # Local scope x
    def f2():
        print(x)        # Reference made in nested def
    f2()

f1()                    # print 88, enclosing def local
