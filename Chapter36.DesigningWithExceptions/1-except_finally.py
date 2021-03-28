#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 1-except_finally.py
# Description: after finally, the exception will be propagated upper 
#------------------------------------------------



def raise1():
    raise IndexError

def noraise():
    return

def raise2():
    raise SyntaxError


for func in raise1, noraise, raise2:
    print('<%s>' % func.__name__)
    try:
        try:
            func()
        except IndexError:
            print('caught IndexError')
    finally:
        print('finally run')
    print('...')
