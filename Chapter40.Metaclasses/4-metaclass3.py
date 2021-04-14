#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 4-metaclass3.py
# Description: factory function as a metaclass
#-------------------------------------------


def metaFunc(classname, supers, classdict):
    print('In metaFunc: ', classname, supers, classdict, sep='\n...')
    return type(classname, supers, classdict)


class Eggs:
    pass


print('Making class: ')
class Spam(Eggs, metaclass=metaFunc):               # Run simple function at end
    data = 1
    def meth(self, arg):
        return self.data + arg



if __name__ == '__main__':
    print('Making instance: ')
    X = Spam()
    print('data: ', X.data, X.meth(2))

    '''
    result: 
    Chapter40.Metaclasses]# python3 4-metaclass3.py
    Making class: 
    In metaFunc: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f40d5d8b280>}
    Making instance: 
    data:  1 3
    '''
