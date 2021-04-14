#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 4-metaclass4-super.py
# Description: instance with superclass as metaclass
#------------------------------------------


'''
In fact, we can use normal superclass inheritance to acquire the call interceptor in this
coding model -- the superclass here is serving essentially the same role as type, at least
in terms of metaclass dispatch
'''


class SuperMetaObj:
    def __call__(self, classname, supers, classdict):
        print('In SuperMetaObj.__call__: ', classname, supers, classdict, sep='\n...')
        klass = self.__New__(classname, supers, classdict)
        self.__Init__(klass, classname, supers, classdict)
        return klass


class SubMetaObj(SuperMetaObj):
    def __New__(self, classname, supers, classdict):
        print('In SubMetaObj.__New__: ', classname, supers, classdict, sep='\n...')
        return type(classname, supers, classdict)

    def __Init__(self, klass, classname, supers, classdict):
        print('In SubMetaObj.__Init__: ', classname, supers, classdict, sep='\n...')
        print('...init class object: ', list(klass.__dict__.keys()))


class Eggs:
    pass


print('Making class: ')
class Spam(Eggs, metaclass=SubMetaObj()):             # Invoke Sub instance via Super.__call__
    data = 1
    def meth(self, arg):
        return self.data + arg



if __name__ == '__main__':
    print('Making instance: ')
    X = Spam()
    print('data: ', X.data, X.meth(2))

    '''
    result: 
    Chapter40.Metaclasses]# python3 4-metaclass4-super.py
    Making class: 
    In SuperMetaObj.__call__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f38d57ea310>}
    In SubMetaObj.__New__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f38d57ea310>}
    In SubMetaObj.__Init__: 
    ...Spam
    ...(<class '__main__.Eggs'>,)
    ...{'__module__': '__main__', '__qualname__': 'Spam', 'data': 1, 'meth': <function Spam.meth at 0x7f38d57ea310>}
    ...init class object:  ['__module__', 'data', 'meth', '__doc__']
    Making instance: 
    data:  1 3
    '''
