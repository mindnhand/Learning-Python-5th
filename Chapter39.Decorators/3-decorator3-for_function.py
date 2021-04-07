#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 3-decorator3.py
# Description: enclosing closure and global
#------------------------------------------


calls = 0


def tracer(func):           # State via enclosing scope and global
    def wrapper(*args, **kwargs):
        global calls
        calls += 1
        print('calls %s to %s' % (calls, func.__name__))
        return func(*args, **kwargs)
    return wrapper

@tracer
def spam(a, b, c):          # Same as: spam = tracer(spam)
    print(a + b + c)


@tracer
def eggs(x, y):             # Same as: eggs = tracer(eggs)
    print(x ** y)


spam(1, 2, 3)               # Really calls wrapper, assigned to spam
spam(a=4, b=5, c=6)         # wrapper calls spam

eggs(2, 16)                 # Really calls wrapper, assigned to eggs
eggs(4, y=7)                # Global calls is not per-decoration here!
