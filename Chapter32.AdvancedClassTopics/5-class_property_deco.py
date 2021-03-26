#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 5-class_property_deco.py
# Description:Because they also accept and return functions, the classmethod 
#             and property built-in functions may be used as decorators in the 
#             same way -- as in the following mutation of the prior bothmethods.py
#-----------------------------------------


class Methods:
    def imeth(self, x):                 # Normal instance method: pass a self
        print([self, x])

    @staticmethod                       # Static method: no instance passed
    def smeth(x):
        print([x])

    @classmethod                        # Class method: pass a cls, not instance
    def cmeth(cls, x):
        print([cls, x])

    @property                           # Property: computed on fetch
    def name(self):
        return 'Bob ' + self.__class__.__name__




if __name__ == '__main__':
    obj = Methods()
    obj.imeth(1)

    Methods.smeth(2)

    Methods.cmeth(3)

    print(obj.name)
