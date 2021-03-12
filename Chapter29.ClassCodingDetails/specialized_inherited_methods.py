#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 specialized_inherited_methods.py
# Description: call super class's method 
#------------------------------------------------



'''
The tree-searching model of inheritance just described turns out to be a great way to
specialize systems. Because inheritance finds names in subclasses before it checks superclasses,
subclasses can replace default behavior by redefining their superclasses' attributes. 
In fact, you can build entire systems as hierarchies of classes, which you
extend by adding new external subclasses rather than changing existing logic in place.
The idea of redefining inherited names leads to a variety of specialization techniques.
For instance, subclasses may replace inherited attributes completely, provide attributes
that a superclass expects to find, and extend superclass methods by calling back to the
superclass from an overridden method. We've already seen some of these patterns in
action; here's a self-contained example of extension at work:
'''


class Super:
    def method(self):
        print('in Super.method')


class Sub(Super):
    def method(self):                           # Override method
        print('Starting Sub.method')            # Add actions here
        Super.method(self)                      # Run default action
        print('Ending Sub.method')



'''
Direct superclass method calls are the crux of the matter here. The Sub class replaces
Super's method function with its own specialized version, but within the replacement,
Sub calls back to the version exported by Super to carry out the default behavior. In
other words, Sub.method just extends Super.method's behavior, rather than replacing it
completely:
'''
print('x is Super class\'s instance')
x = Super()                                     # Make a Super instance
x.method()                                      # Runs Sub.method, calls Super.method
print()

print('y is Sub class\'s instance')
y = Sub()                                       # Make a Sub instance
y.method()                                      # Run Sub.method, call Super.method
# This extension coding pattern is also commonly used with constructors
