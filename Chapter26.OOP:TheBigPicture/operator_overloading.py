#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 operator_overloading.py
# Description: Operator Overload
#--------------------------------------------


'''
As currently coded, our C1 class doesn't attach a name attribute to an instance until the
setname method is called. Indeed, referencing I1.name before calling I1.setname would
produce an undefined name error. If a class wants to guarantee that an attribute like
name is always set in its instances, it more typically will fill out the attribute at construction
time, like this:
'''


class C2:                                   # Make superclass objects
    ...


class C3:
    ...


class C1(C2, C3):
    def __init__(self, who):                # Set name when constructed
        self.name = who                     # Self is either I1 or I2


I1 = C1('bob')
I2 = C1('sue')


print(I1.name)
print(I2.name)
