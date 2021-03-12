#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 classtree.py
# Description: Climb inheritance trees using namespace links,
#              displaying higher superclasses with indentation for height
#----------------------------------------------


def classtree(cls, indent):
    '''
    The classtree function in this script is recursive—it prints a classs's name using
    __name__, then climbs up to the superclasses by calling itself. This allows the function
    to traverse arbitrarily shaped class trees; the recursion climbs to the top, and stops at
    root superclasses that have empty __bases__ attributes. When using recursion, each
    active level of a function gets its own copy of the local scope; here, this means that
    cls and indent are different at each classtree level.
    '''
    print('.' * indent + cls.__name__)                  # Print class name here
    for supercls in cls.__bases__:                      # Recur to all superclasses
        classtree(supercls, indent+3)                   # May visit super > once


def instancetree(inst):
    print('Tree of %s' % inst)                          # Show instance
    classtree(inst.__class__, 3)                        # Climb to its class


def selftest():
    class A:
        pass
    class B(A):
        pass
    class C(A):
        pass
    class D(B, C):
        pass
    class E:
        pass
    class F(D, E):
        pass
    instancetree(B())
    instancetree(F())



if __name__ == '__main__':
    selftest()
