#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3
# Description: class decorator will retain multiple instance
#---------------------------------------------



class Tracer:
    '''
    The following slightly simplified alternative works similarly because its 
    __init__ is triggered when the @ decorator is applied to the class, and its
    __call__ is triggered when a subject class instance is created. 
    '''
    def __init__(self, aClass):             # on @ decoration
        self.aClass = aClass                # use instance attribute
    def __call__(self, *args):              # on instance creation   
        self.wrapped = self.aClass(*args)   # one (last) instance per class
        return self
    def __getattr__(self, attrname):
        print('Trace: ' + attrname)
        return getattr(self.wrapped, attrname)



@Tracer
class Spam:                 # Spam = Tracer(Spam)
    def display(self):
        print('Spam!' * 8)


@Tracer
class Person:               # Person = Tracer(Person)
    def __init__(self, name):       # Wrapper bound to Person
        self.name = name


if __name__ == '__main__':
    food = Spam()
    food.display()

    bob = Person('Bob')             # bob is really a Wrapper
    print(bob.name)                 # Wrapper embeds a Person

    sue = Person('Sue')
    print(sue.name)                 # sue overwrite bob
    print(bob.name)                 # OOPS: now bob's name is 'Sue'!
