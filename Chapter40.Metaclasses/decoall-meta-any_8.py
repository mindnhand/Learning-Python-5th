#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3
# Description: metaclass factory - apply any decorator to all methods of a class
#----------------------------------------------

from types import FunctionType
from decotools_8 import tracer, timer


def decorateAll(decorator):
    class MetaDecorate(type):
        def __new__(meta, clsname, supers, clsdict):
            for attr, attrval in clsdict.items():
                if type(attrval) is FunctionType:
                    clsdict[attr] = decorator(attrval)
            return type.__new__(meta, clsname, supers, clsdict)
    return MetaDecorate


# implementation 1:
class Person1(metaclass=decorateAll(tracer)):            # apply a decorator to all
    def __init__(self, name ,pay):
        self.name = name
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]

# implementation 2:
class Person2(metaclass=decorateAll(timer())):             # apply a decorator to all
    def __init__(self, name ,pay):
        self.name = name
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]

# implementation 3:
class Person3(metaclass=decorateAll(timer(label='**'))): # apply a decorator to all
    def __init__(self, name ,pay):
        self.name = name
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]


if __name__ == '__main__':
    print('\033[1;34mimplementation 1\033[0m')
    bob1 = Person1('Bob Smith', 50000)
    sue1 = Person1('Sue Jones', 100000)
    print(bob1.name, sue1.name)
    sue1.giveRaise(.10)
    print('%.2f' % sue1.pay)
    print(bob1.lastName(), sue1.lastName())


    print('\033[1;34mimplementation 2\033[0m')
    bob2 = Person2('Bob Smith', 50000)
    sue2 = Person2('Sue Jones', 100000)
    print(bob2.name, sue2.name)
    sue2.giveRaise(.10)
    print('%.2f' % sue2.pay)
    print(bob2.lastName(), sue2.lastName())
    print('-'*40)
    print('%.5f' % Person2.__init__.alltime)
    print('%.5f' % Person2.giveRaise.alltime)
    print('%.5f' % Person2.lastName.alltime)


    print('\033[1;34mimplementation 3\033[0m')
    bob3 = Person3('Bob Smith', 50000)
    sue3 = Person3('Sue Jones', 100000)
    print(bob3.name, sue3.name)
    sue3.giveRaise(.10)
    print('%.2f' % sue3.pay)
    print(bob3.lastName(), sue3.lastName())
    print('-'*40)
    print('%.5f' % Person3.__init__.alltime)
    print('%.5f' % Person3.giveRaise.alltime)
    print('%.5f' % Person3.lastName.alltime)

