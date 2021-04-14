#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------
# Usage: python3 4-metaclass2.py
# Description: example for metaclass
#----------------------------------------


class MetaTwo(type):
    '''
    Use both __new__ and __init__ in metaclass

    In this case, the class initialization method is run after the class 
    construction method, but both run at the end of the class statement 
    before any instances are made. Conversely, an __init__ in Spam would 
    run at instance creation time, and is not affected or run by the metaclass's __init__
    '''
    def __new__(meta, classname ,supers, classdict):
        print('In MetaTwo.__new__: ', classname, supers, classdict, sep='\n...')
        return type.__new__(meta, classname, supers, classdict)
    
    def __init__(klass, classname, supers, classdict):
        print('In MetaTwo.__init__: ', classname, supers, classdict, sep='\n...')
        print('...init class object: ', list(klass.__dict__.keys()))


class Eggs:
    pass


print('Making class:')
class Spam(Eggs, metaclass=MetaTwo):                # Inherits from Eggs, instance of MetaTwo
    data = 1            # class data attribute
    def meth(self, arg):    # class method attribute
        return self.data + arg



if __name__ == '__main__':
    print('Making instance: ')
    X = Spam()
    print('data: ', X.data, X.meth(2))

    '''
    result: 
    Chapter40.Metaclasses]# python3 4-metaclass2.py
    Making class:
    In MetaTwo.__new__:
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7fde8294f310>}                                
    In MetaTwo.__init__:
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7fde8294f310>}                                
    ...init class object:  ['__module__', 'data', 'meth', '__doc__']
    Making instance:data:  1 3
    '''
