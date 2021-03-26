#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------
# Usage: python3 mapattrs-slots.py
# Description: test __slots__ attribute inheritance
#-------------------------------------



from mapattrs import mapattrs, trace


class A(object):
    __slots__ = ['a', 'b']
    x = 1
    y = 2


class B(A):
    __slots__ = ['b', 'c']


class C(A):
    x = 2


class D(B, C):
    z = 3
    def __init__(self):
        self.name = 'Bob'



if __name__ == '__main__':
    I = D()
    trace(mapattrs(I, bysource=True))           # Also: trace(mapattrs(I))
