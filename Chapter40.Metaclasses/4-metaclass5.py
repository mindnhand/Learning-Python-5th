#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------
# Usage: python3 4-metaclass5.py
# Description: overloading class creation calls with metaclass
#------------------------------------------------------


'''
Since they participate in normal OOP mechanics, it's also possible for metaclasses to catch 
the creation call at the end of a class statement directly, by redefining the type object's
__call__. The redefinitions of both __new__ and __call__ must be careful to call back to their 
defaults in type if they mean to make a class in the end, and __call__ must invoke type to 
kick off the other two here
'''


# Classes can catch calls too (but built-ins look in metas, not supers!)
class SuperMeta(type):
    def __call__(meta, classname, supers, classdict):
        print('In SuperMeta.__call__: ', classname, supers, classdict, sep='\n...')
        return type.__call__(meta, classname, supers, classdict)

    def __init__(klass, classname, supers, classdict):
        print('In SuperMeta init: ', classname, supers, classdict, sep='\n...')
        print('...init class object: ', list(klass.__dict__.keys()))


print('Making metaclass...')
class SubMeta(type, metaclass=SuperMeta):
    def __new__(meta, classname, supers, classdict):
        print('In SubMeta.__new__: ', classname, supers, classdict, sep='\n...')
        return type.__new__(meta, classname, supers, classdict)

    def __init__(klass, classname, supers, classdict):
        print('In SubMeta init: ', classname, supers, classdict, sep='\n...')
        print('...init class object: ', list(klass.__dict__.keys()))



class Eggs:
    pass




if __name__ == '__main__':
    print('Making class...')
    class Spam(Eggs, metaclass=SubMeta):                # Invoke SubMeta, via SuperMeta.__call__
        data = 1
        def meth(self, arg):
            return self.data + arg

    print('Making instance...')
    X = Spam()
    print('data: ', X.data, X.meth(2))


    '''
    Chapter40.Metaclasses]# python3 4-metaclass5.py
    Making metaclass...
    In SuperMeta init: 
    ...SubMeta
    ...(<class 'type'>,)
    ...{'__module__': '__main__', '__qualname__': 'SubMeta', '__new__': <function SubMeta.__new__ at 0x7f962faa1280>, '__init__': <function SubMeta.__init__ at 0x7f962faa1310>}
    ...init class object:  ['__module__', '__new__', '__init__', '__doc__']
    Making class...
    In SuperMeta.__call__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f962faa13a0>}
    In SubMeta.__new__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f962faa13a0>}
    In SubMeta init: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f962faa13a0>}
    ...init class object:  ['__module__', 'data', 'meth', '__doc__']
    Making instance...
    data:  1 3
    '''

