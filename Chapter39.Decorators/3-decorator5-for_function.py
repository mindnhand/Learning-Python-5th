#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 3-decorator5.py
# Description: function attribution to retain state info for every call
#-----------------------------------------------


def tracer(func):               # State via enclosing scope and function attribute
    def wrapper(*args, **kwargs):       # calls are per-function, not global
        wrapper.calls += 1
        print('call %s to %s' % (wrapper.calls, func.__name__))
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@tracer
def spam(a, b, c):          # Same as: spam = tracer(spam)
    print(a + b + c)


@tracer
def eggs(x, y):             # Same as: eggs = tracer(eggs)
    print(x ** y)



if __name__ == '__main__':
    spam(1, 2, 3)
    spam(a=4, b=5, c=6)

    eggs(2, 16)
    eggs(4, 7)
