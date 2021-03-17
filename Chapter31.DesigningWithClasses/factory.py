#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 factory.py
# Description: factory function
#-------------------------------------------------



def factory(aClass, *pargs, **kargs): 		# Varargs tuple, dict
    return aClass(*pargs, **kargs) 			# Call aClass (or apply in 2.X only)

class Spam:
    def doit(self, message):
        print(message)

class Person:
    def __init__(self, name, job=None):
        self.name = name
        self.job = job



if __name__ == '__main__':
    object1 = factory(Spam) 						# Make a Spam object
    object2 = factory(Person, "Arthur", "King") 	# Make a Person object
    object3 = factory(Person, name='Brian') 		# Ditto, with keywords and default
    object1.doit(99)
    print(object2.name, object2.job)
    print(object3.name, object3.job)
