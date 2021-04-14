#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------
# Usage: python3 7-deco-call-meta.py
# Description: decorator call metaclass, though not vice versa without type()
#----------------------------------------



class MetaClass(type):
    def __new__(meta, classname, supers, attrdict):
        print('\033[1;35mIn metaclass M.__new__: \033[0m')
        print([classname, supers, list(attrdict.keys())])
        return type.__new__(meta, classname, supers, attrdict)

class A:
    x = 1

#************************************************************************
# implementation 1: 
def decorator(cls):
    print('\033[1;35mIn decorator function\033[0m')
    return MetaClass(cls.__name__, cls.__bases__, dict(cls.__dict__))


print('\033[1;34mbefore defination B of implementation 1\033[0m')
@decorator
class B(A):
    print('\033[1;35min class B of implementation 1\033[0m')
    y = 2
    def m(self):
        return self.x + self.y

#************************************************************************
# implementation 2:
print('\033[1;34mbefore defination B of implementation 2\033[0m')
class B(A, metaclass=MetaClass):
    print('\033[1;35min class B of implementation 2\033[0m')
    y = 2
    def m(self):
        return self.x + self.y
#************************************************************************


if __name__ == '__main__':
    print('\033[1;34maccess class attribute: \033[0m')
    print(B.x, B.y)
    print()

    print('\033[1;34mmake instance of class: \033[0m')
    i = B()
    print(i.x, i.y, i.m())

