#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage:
# Description:
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


class Super:
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
    def action(self):
        #assert False, 'action must be defined!'                 # If this version is called
        raise NotImplementedError('This is Super class\'s method, need to implement action in subclass')


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
    for klass in (Inheritor, Replacer, Extender):
        print('\n' + klass.__name__ + '...')
        klass().method()
    print('\nProvider...')
    x = Provider()
    x.delegate()
    print()
    '''
    Of the prior example's classes, Provider may be the most crucial to understand. When
    we call the delegate method through a Provider instance, two independent inheritance
    searches occur:
    1. On the initial x.delegate call, Python finds the delegate method in Super by
       searching the Provider instance and above. The instance x is passed into the
       method's self argument as usual.
    2. Inside the Super.delegate method, self.action invokes a new, independent inheritance
       search of self and above. Because self references a Provider instance,
       the action method is located in the Provider subclass.

    This "filling in the blanks" sort of coding structure is typical of OOP frameworks. In a
    more realistic context, the method filled in this way might handle an event in a GUI,
    provide data to be rendered as part of a web page, process a tag's text in an XML file,
    and so on—your subclass provides specific actions, but the framework handles the rest
    of the overall job.
    '''

    #print('with the instance of Super class')
    #y = Super()
    #y.delegate()
    #print()

    print('Inheritor class instance call delegate method')
    z = Inheritor()
    z.delegate()
