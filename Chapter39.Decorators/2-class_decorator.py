#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------
# Usage: python3 1-class_decoratory.py
# Description: define and use a class decorator
#----------------------------------


# 1. define a class decorator
def decorator(cls):     # on @ decoration
    class Wrapper:
        def __init__(self, *args):          # on instance creation
            print('in decorator.Wrapper.__init__')
            self.wrapped = cls(*args)
        def __getattr__(self, name):        # on attribute fetch
            print('in decorator.Wrapper.__getattr__')
            return getattr(self.wrapped, name)
    return Wrapper



# 2. define the decorated class
@decorator
class C:            # on C = decorator(C)
    def __init__(self, x, y):               # run by Wrapper.__init__
        print('in the decorated class.__init__')
        self.attr = 'spam'



if __name__ == '__main__':
    x = C(6, 7)             # Really calls Wrapper(6, 7)
    print(x.attr)           # Runs Wrapper.__getattr__, print spam
    print(dir(x))
