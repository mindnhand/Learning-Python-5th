#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 4-metaclass5b.py
# Description: a normal superclass is skipped for built-ins, but not for explicit fetches
#              and calls, the latter relying on normal attribute name inheritance
#-------------------------------------------



class SuperMeta(type):
    def __call__(meta, classname, supers, classdict):           # By name, not builtin
        print('In SuperMeta.__call__: ', classname)
        return type.__call__(meta, classname, supers, classdict)


class SubMeta(SuperMeta):               # Created by type default
    def __init__(klass, classname, supers, classdict):          # Overrides type.__init__
        print('In SubMeta.__init__: ', classname)


if __name__ == '__main__':
    print(SubMeta.__class__)
    print([n.__name__ for n in SubMeta.__mro__])
    print()
    print(SubMeta.__call__)             # Not a data descriptor if found by name
    print()
    SubMeta.__call__(SubMeta, 'XXX', (), {})        # Explicit call works: class inheritance
    print()
    SubMeta('yyy', (), {})


    '''
    Chapter40.Metaclasses]# python3 4-metaclass5b.py
    <class 'type'>
    ['SubMeta', 'SuperMeta', 'type', 'object']

    <function SuperMeta.__call__ at 0x7f49b77a3d30>

    In SuperMeta.__call__:  XXX
    In SubMeta.__init__:  XXX

    In SubMeta.__init__:  yyy
    '''
