#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 4-bothmethods.py
# Description: we can code classes with static and class methods, neither of 
#              which requires an instance argument to be passed in when invoked. 
#              To designate such methods, classes call the built-in functions 
#              staticmethod and classmethod, as hinted in the earlier discussion 
#              of new-style classes. Both mark a function object as special -- that 
#              is, as requiring no instance if static and requiring a class argument 
#              if a class method.
#-----------------------------------------



class Methods:
    def imeth(self, x):             # Normal instance method: passed a self
        print([self, x])
    def smeth(x):                   # Static method: no instance is passed in
        print([x])
    def cmeth(cls, x):              # Class method: get class, not instance 
        print([cls, x])
    smeth = staticmethod(smeth)     # make smeth a static method, or by @ ahead
    cmeth = classmethod(cmeth)      # make cmeth a class method, or by @ ahead


if __name__ == '__main__':
    print('instance method' + '=' * 20)
    obj = Methods()
    obj.imeth(4)
    Methods.imeth(obj, 4)
    print()

    print('static method' + '=' * 20)
    Methods.smeth(5)
    obj.smeth(5)
    print()


    print('class method' + '=' * 20)
    '''
    Class methods are similar, but Python automatically passes the class (not an instance) 
    in to a class method's first (leftmost) argument, whet her it is called through a class
    or an instance
    '''
    Methods.cmeth(6)
    obj.cmeth(6)
