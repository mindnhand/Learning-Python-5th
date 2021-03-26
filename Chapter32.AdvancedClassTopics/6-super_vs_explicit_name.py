#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------
# Usage: python3 6-super_vs_explicit_name.py
# Description: super call VS. explicit-name
#------------------------------------



'''
In diamond class tree patterns, though, explicit-name calls may by default 
trigger the top-level class's method more than once, though this might be 
subverted with additional protocols (e.g., status markers in the instance)

By contrast, if all classes use super, or are appropriately coerced by proxies 
to behave as if they do, the method calls are dispatched according to class 
order in the MRO, such that the top-level class's method is run just once

The real magic behind this is the linear MRO list constructed for the class 
of self -- because each class appears just once on this list, and because 
super dispatches to the next class on this list, it ensures an orderly 
invocation chain that visits each class just once. Crucially, the next class 
following B in the MRO differs depending on the class of self -- it's A for a 
B instance, but C for a D instance, accounting for the order of constructors run
'''

# 1. Explicit name
class A:
    def __init__(self):
        print('Create instance of class A', end=': ')
        print('A.__init__')

class B(A):
    def __init__(self):
        print('Create instance of class B', end=': ')
        print('B.__init__')
        A.__init__(self)

class C(A):
    def __init__(self):
        print('Create instance of class C', end=': ')
        print('C.__init__')
        A.__init__(self)


class D(B, C):
    pass


class D1(B, C):
    def __init__(self):
        print('Create instance of class D1', end=': ')
        B.__init__(self)
        C.__init__(self)

# 2. super call
class BS(A):
    def __init__(self):
        print('Create instance of class BS', end=': ')
        print('BS.__init__')
        super().__init__()

class CS(A):
    def __init__(self):
        print('Create instance of class CS', end=': ')
        print('CS.__init__')
        super().__init__()


class DS(BS, CS):
    pass


class DS1(BS, CS):
    def __init__(self):
        print('Create instance of class DS1', end=': ')
        super().__init__()
        super().__init__()



if __name__ == '__main__':
    print('instance x1 = B()')
    x1 = B()

    print('instance x2 = C()')
    x2 = C()

    print('instance x3 = D()')
    x3 = D()
    print()

    print('After redefine __init__ operator in class D')
    x4 =D1()
    print('The MRO of B is: ', B.__mro__)
    print('The MRO of D is: ', D.__mro__)
    print('=' * 40)


    print('Test for super')
    print('instance x1 = BS()')
    x1 = BS()

    print('instance x2 = CS()')
    x2 = CS()

    print('instance x3 = DS()')
    x3 = DS()
    print()

    print('After redefine __init__ operator in class DS1')
    x4 =DS1()

    print('The MRO of BS is: ', BS.__mro__)
    print('The MRO of DS is: ', DS.__mro__)
