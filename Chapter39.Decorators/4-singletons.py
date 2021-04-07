#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 4-singletons.py
# Description: singleton class
#----------------------------------------------





# enclosing function and global instances
instances = {}
def singleton(aClass):              # on @ decoration
    print('in decorator singleton')
    def onCall(*args, **kwargs):    # on instance creation
        print('in decorator embeded onCall singleton')
        if aClass not in instances: # one dict entry per class
            instances[aClass] = aClass(*args, **kwargs)
        return instances[aClass]
    return onCall


# enclosing function and nonlocal instance
def singleton1(aClass):
    instance = None
    def onCall(*args, **kwargs):        # on instance creation
        nonlocal instance
        if instance == None:
            instance = aClass(*args, **kwargs)          # one scope per class
        return instance
    return onCall


# enclosing function and function attributes
def singleton2(aClass):
    def onCall(*args, **kwargs):        # on instance creation
        if onCall.instance == None:
            onCall.instance = aClass(*args, **kwargs)   # one function per class
        return onCall.instance
    onCall.instance = None
    return onCall


# class with __call__ method
class singleton3(aClass):
    def __init__(self, aClass):                 # on @ decoration
        self.aClass = aClass
        self.instance = None
    def __call__(self, *args, **kwargs):        # on instance creation
        if self.instance == None:
            self.instance = self.aClass(*args, **kwargs)        # one instance per class
        return self.instance


@singleton
class Person:               # rebind Person to onCall
    def __init__(self, name, hours, rate):      # onCall remembers Person
        print('in Person.__init__')
        self.name = name
        self.hours = hours
        self.rate = rate
    def pay(self):
        print('in Person.pay')
        return self.hours * self.rate


@singleton
class Spam:                 # rebind Spam to onCall
    def __init__(self, val):        # onCall remembers Spam
        print('in Spam.__init__')
        self.attr = val


if __name__ == '__main__': 
    bob = Person('Bob', 40, 10)         # really calls onCall
    print(bob.name, bob.pay())
    
    sue = Person('Sue', 50, 20)
    print(sue.name, sue.pay())

    X = Spam(val=42)            # one Person, one Spam
    Y = Spam(99)
    print(X.attr, Y.attr)
