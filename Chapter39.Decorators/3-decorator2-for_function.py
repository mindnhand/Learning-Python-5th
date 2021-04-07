#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 3-decorator2.py
# Description: Tracer call with key-word only
#------------------------------------------------


class Tracer:           # state via instance attributes
    def __init__(self, func):           # on @ decorator
        self.func = func
        self.calls = 0                  # save func for later call
    def __call__(self, *args, **kwargs):
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)



@Tracer
def spam(a, b, c):          # Same as: spam = Tracer(spam)
    print(a + b + c)        # Triggers Tracer.__init__


@Tracer
def eggs(x, y):             # Same as: eggs = Tracer(eggs)
    print(x ** y)           # Wrap eggs in Tracer object



if __name__ == '__main__':
    spam(1, 2, 3)           # Really calls Tracer instance: runs tracer.__call__
    spam(a=4, b=5, c=6)     # spam is an instance attribute

    eggs(2, 16)             # Really calls Tracer instance, self.func is eggs
    eggs(4, y=7)            # self.calls is per-decoration here
