#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 4-metaclass1.py
# Description: example for metaclass
#-------------------------------------------------


class MetaOne(type):
    '''
    Use only __new__ in metaclass
    '''
    def __new__(meta, classname, supers, classdict):
        print('In MetaOne.new: ', meta, classname, supers, classdict, sep='\n...')
        return type.__new__(meta, classname, supers, classdict)


class Eggs:
    pass


print('Making class')
class Spam(Eggs, metaclass=MetaOne):            # Inherits from Eggs, instance of MetaOne
    data = 1            # class data attribute
    def meth(self, arg):            # class method attribute
        return self.data + arg



if __name__ == '__main__':
    print('making instance')
    X = Spam()
    print('data: ', X.data, X.meth(2))

    '''
    result:
    Chapter40.Metaclasses]# python3 4-metaclass1.py
    Making class
    In MetaOne.new:
    ...<class '__main__.MetaOne'>
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f90d6d4f280>}                                
    making instance
    data:  1 3
    '''
