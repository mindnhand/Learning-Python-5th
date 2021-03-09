#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------
# Usage: python3 class_tree.py
# Description: Class Tree
#----------------------------------------



class C2:                               # Make superclass objects
    ...

class C3:
    ...


class C1(C2, C3):                       # Make and link class C1
    '''
    There's nothing syntactically unique about def in this context. Operationally, though,
    when a def appears inside a class like this, it is usually known as a method, and it
    automatically receives a special first argument--alled self by convention--that provides
    a handle back to the instance to be processed. Any values you pass to the method
    yourself go to arguments after self (here, to who).
    Because classes are factories for multiple instances, their methods usually go through
    this automatically passed-in self argument whenever they need to fetch or set attributes
    of the particular instance being processed by a method call. In the preceding code,
    self is used to store a name in one of two instances.
    '''
    def setname(self, who):             # Assign name: C1.setname
        self.name = who                 # Self is either I1 or I2



I1 = C1()                               # Make two instances
I2 = C1()


I1.setname('bob')                       # Set I1.name to 'bob'
I2.setname('sue')                       # Set I2.name to 'sue'

print(I1.name)
print(I2.name)
