#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------
# Usage: python3 3-display_exception.py
# Description: display exceptions
#---------------------------------------



class E(Exception):
    pass


try:
    raise E('spam')
except E as X:
    print(X)
    print(X.args)
    print(repr(X))
finally:
    print()

try:
    raise E('spam', 'eggs', 'ham')
except E as X:
    print('%s %s' % (X, X.args))
finally:
    print()
