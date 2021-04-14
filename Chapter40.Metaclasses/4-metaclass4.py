#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 4-metaclass4.py
# Description: class instance as metaclass
#-----------------------------------------


'''
Because normal class instances can respond to call operations with operator overloading, 
they can serve in some metaclass roles too, much like the preceding function. The output 
of the following is similar to the prior class-based versions, but it's based on a simple 
class -- one that doesn't inherit from type at all, and provides a __call__ for its instances 
that catches the metaclass call using normal operator overloading. Note that __new__ 
and __init__ must have different names here, or else they will run when the Meta instance is
created, not when it is later called in the role of metaclass
'''


class MetaObj:
    '''
    A normal class instance can serve as a metaclass too
    '''
    def __call__(self, classname, supers, classdict):
        print('In MetaObj.__call__: ', classname, supers, classdict, sep='\n...')
        klass = self.__New__(classname, supers, classdict)
        self.__Init__(klass, classname, supers, classdict)
        return klass

    def __New__(self, classname, supers, classdict):
        print('In MetaObj.__New__: ', classname, supers, classdict, sep='\n...')
        return type(classname, supers, classdict)

    def __Init__(self, klass, classname, supers, classdict):
        print('In MetaObj.__Init__: ', classname, supers, classdict, sep='\n...')
        print('...init class object: ', list(klass.__dict__.keys()))



class Eggs:
    pass


print('Making class: ')
class Spam(Eggs, metaclass=MetaObj()):              # MetaObj() is a normal class instance
    data = 1                                        # called at the end of the statement
    def meth(self, arg):
        return self.data + arg



if __name__ == '__main__':
    print('Making instance: ')
    X = Spam()
    print('data: ', X.data, X.meth(2))

    '''
    result: 
    Chapter40.Metaclasses]# python3 4-metaclass4.py
    Making class: 
    In MetaObj.__call__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f889a99d3a0>}
    In MetaObj.__New__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f889a99d3a0>}
    In MetaObj.__Init__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f889a99d3a0>}
    ...init class object:  ['__module__', 'data', 'meth', '__doc__']
    Making instance: 
    data:  1 3
    '''
