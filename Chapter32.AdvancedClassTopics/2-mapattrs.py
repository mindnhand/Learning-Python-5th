#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 mapattrs.py
# Description: mapattrs function demonstrates how inheritance actually searches for
#              attributes in class tree objects, though the new-style MRO is largely
#              automated for us
#--------------------------------------------



"""
File mapattrs.py (3.X + 2.X)
Main tool: mapattrs() maps all attributes on or inherited by an
instance to the instance or class from which they are inherited.
Assumes dir() gives all attributes of an instance. To simulate
inheritance, uses either the class's MRO tuple, which gives the
search order for new-style classes (and all in 3.X), or a recursive
traversal to infer the DFLR order of classic classes in 2.X.
Also here: inheritance() gives version-neutral class ordering;
assorted dictionary tools using 3.X/2.7 comprehensions.
"""


import pprint


def trace(x, label='', end='\n'):               # print nicely
    print(label + pprint.pformat(x) + end)


def filterdictvals(d, v):
    '''
    dict D with entries for value V removed.
    filterdictvals(dict(a=1, b=2, c=1), 1) => {'b': 2}
    '''
    return {k: v2 for (k, v2) in d.items() if v2 != v}


def invertdict(d):
    '''
    dict D with values changed to keys (grouped by values).
    Values must all be hashable to work as dict/set keys.
    invertdict(dict(a=1, b=2, c=1)) => {1: ['a', 'c'], 2: ['b']}
    '''
    def keysof(v):
        return sorted(k for k in d.keys() if d[k] == v)         # sorted() return a list
    return {v: keysof(v) for v in set(d.values())}              # set(d.values()): remove duplicate values


def dflr(cls):
    '''
    Classic depth-first left-to-right order of class tree at cls.
    Cycles not possible: Python disallows on __bases__ changes.
    '''
    here = [cls]
    for sup in cls.__bases__:
        here += dflr(sup)           # recursive 
    return here


def inheritance(instance):
    '''
    Inheritance order sequence: new-style (MRO) or classic (DFLR)
    '''
    if hasattr(instance.__class__, '__mro__'):
        return (instance,) + instance.__class__.__mro__
    else:
        return [instance] + dflr(instance.__class__)


def mapattrs(instance, withobject=False, bysource=False):
    '''
    dict with keys giving all inherited attributes of instance,
    with values giving the object that each is inherited from.
    withobject: False=remove object built-in class attributes.
    bysource: True=group result by objects instead of attributes.
    Supports classes with slots that preclude __dict__ in instances.
    '''
    attr2obj = {}
    inherits = inheritance(instance)
    for attr in dir(instance):
        for obj in inherits:
            if hasattr(obj, '__dict__') and attr in obj.__dict__:       # see slots
                attr2obj[attr] = obj
                break

    if not withobject:
        attr2obj = filterdictvals(attr2obj, object)

    return attr2obj if not bysource else invertdict(attr2obj)




if __name__ == '__main__':
    print('Classic classes in 2.x, new-style in 3.x')
    class A:
        attr1 = 1

    class B(A):
        attr2 = 2

    class C(A):
        attr1 = 3

    class D(B, C):
        pass

    I = D()

    print('Py=>%s' % I.attr1)

    trace(inheritance(I), 'INH\n')              # [Inheritance order]
    trace(mapattrs(I), 'ATTRS\n')               # Attrs => Source
    trace(mapattrs(I, bysource=True), 'OBJS\n') # Source => [Attrs]

    print('New-style classes in 2.x and 3.x')
    class A(object):
        attr1 = 1

    class B(A):
        attr2 = 2

    class C(A):
        attr1 = 3
        
    class D(B, C):
        pass

    I = D()

    print('Py=>%s' % I.attr1)
    trace(inheritance(I), 'INH\n')
    trace(mapattrs(I), 'ATTRS\n')
    trace(mapattrs(I, bysource=True), 'OBJS\n')
