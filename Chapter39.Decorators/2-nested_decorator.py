#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 1-nested_decorator.py
# Description: define multiple nested decorator
#--------------------------------------------


# implementation 1
def deco1(func):
    print('decorate %s in deco1' % func.__name__)
    return func

def deco2(func):
    print('decorate %s in deco2' % func.__name__)
    return func

def deco3(func):
    print('decorate %s in deco3' % func.__name__)
    return func



@deco1
@deco2
@deco3
def func():             # func = d1(d2(d3(func))
    print('in the original function')
    print('spam')

print('\n' + '*-*' * 20 + '\n')

# implementation 2
def deco4(func):
    print('decorate %s in deco4' % func.__name__)
    return lambda: 'X' + func()

def deco5(func):
    print('decorate %s in deco5' % func.__name__)
    return lambda: 'Y' + func()

def deco6(func):
    print('decorate %s in deco6' % func.__name__)
    return lambda: 'Z' + func()


@deco4
@deco5
@deco6
def func1():
    print('in the original function')
    return 'spam'

print('\n' + '*-*' * 20 + '\n')

if __name__ == '__main__':
    print('\033[1;31mImplementation 1\033[0m')
    func()
    print()

    print('\033[1;31mImplementation 1\033[0m')
    print(func1())
