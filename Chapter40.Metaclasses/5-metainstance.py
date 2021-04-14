#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 5-metainstance.py
# Description: metaclass' attribute can't be passed to the latter class' instance
#--------------------------------------------



class MetaOne(type):
    def __new__(meta, classname, supers, classdict):            # Redefine type method
        print('In MetaOne.__new__: ', classname)
        return type.__new__(meta, classname, supers, classdict)

    def toast(self):
        return 'toast'



class Super(metaclass=MetaOne):           # Metaclass inherited by subs too
    def spam(self):                       # MetaOne run twice for two classes
        return 'spam'


class Sub(Super):                         # Superclass: inheritance versus instance
    def eggs(self):                       # Classes inherit from superclasses
        return 'eggs'



if __name__ == '__main__':
    import sys
    print('through instance to access attributes')
    x = Sub()
    print(x.eggs())
    print(x.spam())
    try:
        print(x.toast())
    except:
        print(sys.exc_info())
    print()

    print('through class to access attributes')
    print(Sub.eggs(x))
    print(Sub.spam(x))
    print(Sub.toast())
    try:
        print(Sub.toast(x))
    except:
        print(sys.exc_info())

    '''
    Chapter40.Metaclasses]# python3 5-metainstance.py
    In MetaOne.__new__:  Super
    In MetaOne.__new__:  Sub
    through instance to access attributes
    eggs
    spam
    (<class 'AttributeError'>, AttributeError("'Sub' object has no attribute 'toast'"), <traceback object at 0x7f6e772fae80>)

    through class to access attributes
    eggs
    spam
    toast
    (<class 'TypeError'>, TypeError('toast() takes 1 positional argument but 2 were given'), <traceback object at 0x7f6e772faec0>)
    '''
