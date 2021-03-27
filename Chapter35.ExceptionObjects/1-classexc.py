#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 1-classexc.py
# Description: Exception and categories
#---------------------------------------------


'''
we define a superclass called General and two subclasses called Specific1 
and Specific2. This example illustrates the notion of exception categories
-- General is a category name, and its two subclasses are specific types of 
exceptions within the category. Handlers that catch General will also catch 
any subclasses of it, including Specific1 and Specific2:
'''


class General(Exception):
    pass

class Specific1(General):
    pass

class Specific2(General):
    pass



def raiser0():
    X = General()                   # Raise superclass instance
    raise X


def raiser1():
    X = Specific1()                 # Raise subclass instance
    raise X


def raiser2():
    X = Specific2()                 # Raise different subclass instance
    raise X



if __name__ == '__main__':
    for func in (raiser0, raiser1, raiser2):
        try:
            func()
        except General:             # Match General or any subclass of it
            import sys
            print('caught: %s' % sys.exc_info()[0])
