#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 7-extend-deco.py
# Description: extend with a decorator: same as provides __init__ in metaclass
#----------------------------------------------



def eggsfunc(obj):
    return obj.value * 4


def hamfunc(obj, value):
    return value + 'ham'


def extender(klass):
    klass.eggs = eggsfunc       # manage class, not instance
    klass.ham = hamfunc         # equiv to metaclass __init__
    return klass


@extender
class Client1:                  # Client1 = extender(Client1)
    def __init__(self, value):  # rebound at end of class stmt
        self.value = value
    def spam(self):
        return self.value * 2


@extender
class Client2:
    value = 'ni?'



x = Client1('Ni!')              # x is instance of Client1
print(x.spam())
print(x.eggs())
print(x.ham('bacon'))


y = Client2()
print(y.eggs())
print(y.ham('bacon'))
        
