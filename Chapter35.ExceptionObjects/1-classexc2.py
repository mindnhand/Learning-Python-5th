#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 1-classexc2.py
# Description: raise Exception instance
#----------------------------------------------


'''
we can be sure that the instance raised is an instance of the class listed in
the except, or one of its more specific subclasses. Because of this, the __class__
attribute of the instance also gives the exception type.
'''


class General(Exception):
    pass

class Specific1(General):
    pass

class Specific2(General):
    pass



def raiser0():
    raise General()

def raiser1():
    raise Specific1()

def raiser2():
    raise Specific2()


if __name__ == '__main__':
    for func in raiser0, raiser1, raiser2:
        try:
            func()
        except General as X:                    # X is the raised instance
            print('caught: %s' % X.__class__)   # Same as sys.exc_info()[0]
