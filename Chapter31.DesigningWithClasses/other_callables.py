#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 other_callables.py
# Description: function, instance, method, class
#----------------------------------------------



def square(arg):
    return arg ** 2   	# Simple functions (def or lambda)


class Sum:
    def __init__(self, val):  # Callable instances
        self.val = val
    def __call__(self, arg):
        return self.val + arg


class Product:
    def __init__(self, val): # Bound methods
        self.val = val
    def method(self, arg):
        return self.val * arg


class Negate:
    def __init__(self, val): 		# Classes are callables too
        self.val = -val 	# But called for object, not work
    def __repr__(self): 	# Instance print format
        return str(self.val)



if __name__ == '__main__':
    sobject = Sum(2)
    pobject = Product(3)
    actions = [square, sobject, pobject.method] 	# Function, instance, method
    for act in actions: 	# All three called same way
        print(act(5)) 		# Call any one-arg callable
    
    print(actions[-1](5)) 	# Index, comprehensions, maps
    print([act(5) for act in actions])
    print(list(map(lambda act: act(5), actions)))


    actions = [square, sobject, pobject.method, Negate] 		# Call a class too
    for act in actions:
        print(act(5))
    print([act(5) for act in actions]) 		     # Runs __repr__ not __str__!       print(act(5))
    table = {act(5): act for act in actions}         # 3.X/2.7 dict comprehension
    for (key, value) in table.items():
        print('{0} => {1}'.format(key, value)) 		# 2.6+/3.X str.format
