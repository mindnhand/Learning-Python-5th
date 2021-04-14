#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 decoall-meta_8.py
# Description: metaclass add tracer decorator to every method of a client class
#------------------------------------------------



from types import FunctionType
from decotools_8 import tracer


class MetaTrace(type):
    def __new__(meta, clsname, supers, clsdict):
        for attr, attrval in clsdict.items():
            if type(attrval) is FunctionType:            # Method?
                clsdict[attr] = tracer(attrval)          # Decorate it
        return type.__new__(meta, clsname, supers, clsdict)         # make classes


class Person(metaclass=MetaTrace):
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]



if __name__ == '__main__':
    bob = Person('Bob Smith', 50000)
    sue = Person('Sue Jones', 100000)
    print(bob.name, sue.name)
    sue.giveRaise(.10)
    print('%.2f' % sue.pay)
    print(bob.lastName(), sue.lastName())
