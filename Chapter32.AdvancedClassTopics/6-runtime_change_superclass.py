#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------
# Usage: python3 6-runtime_change_superclass.py
# Description: Superclass that might be changed at runtime dynamically preclude hardcoding
#              their names in a subclass's methods, while super will happily look up the
#              current superclass dynamically. Still, this case may be too rare in practice 
#              to warrant the super model by itself, and can often be implemented in other 
#              ways in the exceptional cases where it is needed. To illustrate, the following 
#              changes the superclass of C dynamically by changing the subclass's __bases__ 
#              tuple in 3.X
#--------------------------------------


class X:
    def m(self):
        print("X.m")
    

class Y:
    def m(self):
        print('Y.m')


class C(X):
    def m(self):            # Start out inheriting from X
        super().m()         # Can't superclass  at runtime
        #C.__bases__[0].m(self)      # The same efffect with the above 




if __name__ == '__main__':
    i = C()
    i.m()

    C.__bases__ = (Y,)       # Change superclass at runtime
    i.m()

    '''
    In [46]: type(a)
    Out[46]: __main__.Age

    In [47]: a.__class__.__bases__
    Out[47]: (object,)

    In [48]: a.__class__.__base__
    Out[48]: object
    '''
