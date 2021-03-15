#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 number.py
# Description: constructor and expression: __init__ and __sub__
#-----------------------------------------------



class Number:
    def __init__(self, start):                      # On number(start)
        '''
        Technically, instance creation first triggers the __new__ method, which
        creates and returns the new instance object, which is then passed into
        __init__ for initialization. Since __new__ has a built-in implementation
        and is redefined in only very limited roles, though, nearly all Python
        classes initialize by defining an __init__ method. We'll see one use case
        for __new__ when we study metaclasses in Chapter 40; though rare, it is
        sometimes also used to customize creation of instances of mutable
        types.
        '''
        self.data = start
    def __sub__(self, other):                       # On instance - other
        '''
        The __sub__ method plays the binary operator role that __add__ did in
        Chapter 27's introduction, intercepting subtraction expressions and returning a new
        instance of the class as its result (and running __init__ along the way).
        '''
        return Number(self.data - other)            # Result is a new instance



if __name__ == '__main__':
    x = Number(5)                                   # Number.__init__(x, 5)
    y = x - 2                                       # Number.__sub__(x, 2), and y is a new Number instance
    print(x.data)
