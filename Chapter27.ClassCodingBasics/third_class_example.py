#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 third_class_example.py
# Description: Operator overload
#---------------------------------------------------



from second_class_example import SecondClass



class ThirdClass(SecondClass):                          # Inherit from SecondClass
    def __init__(self, value):                          # On 'ThirdClass(value)'
        self.data = value
    def __add__(self, other):                           # On 'self + other'
        return ThirdClass(self.data + other)
    def __str__(self):                                  # On 'print(self)', 'str()'
        return '[ThirdClass: %s]' % self.data
    def mul(self, other):
        self.data *= other



if __name__ == '__main__':
    a = ThirdClass('abc')                               # __init__ method is called
    a.display()                                         # Inherited method is called
    print(a)                                            # __str__ method is called: return display string

    b = a + 'xyz'                                       # __add__ method is called, and make a new object
    b.display()                                         # b has all ThirdClass methods
    print(b)                                            # __str__ method is called, return display string

    a.mul(3)                                            # mul method is called, change instance in place
    print(a)
