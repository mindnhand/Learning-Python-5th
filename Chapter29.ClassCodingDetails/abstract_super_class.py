#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: abstract_super_class.py
# Description: abstract super class
#-------------------------------------------



'''
Class Interface Techniques

Extension is only one way to interface with a superclass. The file shown in this section,
specialize.py, defines multiple classes that illustrate a variety of common techniques:
    > Super
         Defines a method function and a delegate that expects an action in a subclass.
    > Inheritor
         Doesn't provide any new names, so it gets everything defined in Super.
    > Replacer
         Overrides Super's method with a version of its own.
    > Extender
         Customizes Super's method by overriding and calling back to run the default.
    > Provider
         Implements the action method expected by Super's delegate method.

Study each of these subclasses to get a feel for the various ways they customize their
common superclass. Here’s the file:
'''

from abc import ABCMeta, abstractmethod


class Super(metaclass=ABCMeta):
    '''
    As of Python 2.6 and 3.0, the prior section's abstract superclasses (a.k.a. "abstract base
    classes", which require methods to be filled in by subclasses, may also be implemented
    with special class syntax. The way we code this varies slightly depending on the version.
    In Python 3.X, we use a keyword argument in a class header, along with special @
    decorator syntax, both of which we’ll study in detail later in this book:
    '''
    def method(self):
        print('in Super.method')                                # Default behavior
    def delegate(self):
        '''
        At least in terms of the delegate method, the superclass in this example is what is
        sometimes called an abstract superclass—a class that expects parts of its behavior to be
        provided by its subclasses. If an expected method is not defined in a subclass, Python
        raises an undefined name exception when the inheritance search fails.
        Class coders sometimes make such subclass requirements more obvious with assert
        statements, or by raising the built-in NotImplementedError exception with raise statements.
        We’ll study statements that may trigger exceptions in depth in the next part of
        this book; as a quick preview, here’s the assert scheme in action:
        '''
        self.action()                                           # Expected to be defined

    @abstractmethod
    def action(self):
        #assert False, 'action must be defined!'                 # If this version is called
        #raise NotImplementedError('This is Super class\'s method, need to implement action in subclass')
        pass
    '''
    Coded this way, a class with an abstract method cannot be instantiated (that is, we
    cannot create an instance by calling it) unless all of its abstract methods have been
    defined in subclasses. Although this requires more code and extra knowledge, the potential
    advantage of this approach is that errors for missing methods are issued when
    we attempt to make an instance of the class, not later when we try to call a missing
    method. This feature may also be used to define an expected interface, automatically
    verified in client classes.
    '''


class Inheritor(Super):                                         # Inherit method verbatim
    pass


class Replacer(Super):                                          # Replace method completely
    def method(self):
        print('in Replacer.method')


class Extender(Super):                                          # Extend method behavior
    def method(self):
        print('Starting Extender.method')
        Super.method(self)
        print('Ending Extender.method')


class Provider(Super):                                          # Fill in a required method
    def action(self):
        print('in Provider.action')



if __name__ == '__main__':
    #x = Super()
    '''
    Traceback (most recent call last):
      File "abstract_super_class.py", line 88, in <module>
          x = Super()
          TypeError: Can't instantiate abstract class Super with abstract methods action
    '''

    #y = Inheritor()
    '''
    Traceback (most recent call last):
      File "abstract_super_class.py", line 96, in <module>
          y = Inheritor()
          TypeError: Can't instantiate abstract class Inheritor with abstract methods action
    '''

    z = Provider()                                              # This will not raise Exception, because there is an action method implemented in Provider class
    z.delegate()
