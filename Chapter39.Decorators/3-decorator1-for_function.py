#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 3-decorator1.py
# Description: Tracing calls
#----------------------------------------------


# 1. function decorator
class Tracer:
    def __init__(self, func):       # On @ decoration: save original func
        print('In the decorator __init__ method')
        self.calls = 0
        self.func = func
    def __call__(self, *args):      # on later calls: run original func
        print('In the decorator __call__ method')
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)



@Tracer
def spam(a, b, c):                  # spam = Tracer(spam)
    print('In the decorated function spam')
    print(a + b + c)                # Wrap spam in a decorator object


# 2. directy call 
call_num = 0

def tracer(func, *args):
    global call_num
    call_num += 1
    print('call %s to %s' % (call_num, func.__name__))
    func(*args)


def spam1(a, b, c):
    print(a + b + c)


if __name__ == '__main__':
    print('\n\033[1;35mEntrance\033[0m\n')
    print('\033[1;37mfunction decorator\033[0m')
    spam(1, 2, 3)
    spam('a', 'b', 'c')

    print()
    print('\033[1;37mdirectly call\033[0m')
    tracer(spam1, 1, 2, 3)
