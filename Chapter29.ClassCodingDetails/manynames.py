#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 manynames.py
# Description: namespace and scope
#------------------------------------------


x = 11                                      # Global (module) name/attribute (x, or manynames.x)

def f():
    print(x)                                # Access global x (11)


def g():
    x = 22                                  # Local (function) variable (x, hides module x)
    print(x)


class C:
    x = 33                                  # Class attribute
    def m(self):
        x = 44                              # Local variable in method (x)
        self.x = 55                         # Instance attribute (instance.x)


'''
From top to bottom, the assignments to X here generate: a module attribute (11), 
a local variable in a function (22), a class attribute (33), a local variable in 
a method (44), and an instance attribute (55). Although all five are named X, 
the fact that they are all assigned at different places in the source
code or to different objects makes all of these unique variables.

You should take the time to study this example carefully because it collects ideas we've
been exploring throughout the last few parts of this book. When it makes sense to you,
you will have achieved Python namespace enlightenment. Or, you can run the code
and see what happens—heree's the remainder of this source file, which makes an instance
and prints all the Xs that it can fetch:
'''


if __name__ == '__main__':
    print(x)                                # 11: module (a.k.a manynames.x outside file)
    f()                                     # 11: global
    g()                                     # 22: local
    print(x)                                # 11: module name unchanged

    obj = C()                               # Make instance
    print(obj.x)                            # 33: class name inherited by instance

    obj.m()                                 # Attach attribute name x to instance now
    print(obj.x)                            # 55: instance
    print(C.x)                              # 33: class (a.k.a obj.x if no x in instance)

    '''
    The outputs that are printed when the file is run are noted in the comments in the code;
    trace through them to see which variable named X is being accessed each time. Notice
    in particular that we can go through the class to fetch its attribute (C.X), but we can
    never fetch local variables in functions or methods from outside their def statements.
    Locals are visible only to other code within the def, and in fact only live in memory
    while a call to the function or method is executing.
    '''
