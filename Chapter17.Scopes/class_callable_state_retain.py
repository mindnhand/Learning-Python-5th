#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 class_callable_state_retain.py
# Description: with class, carry out multi-state retain
#---------------------------------------------------




# with class, will carry out multi-state retain
class tester():             # class tester:
    '''
    use classes with attributes to make state information access more explicit than the implicit
    magic of scope lookup rules. As an added benefit, each instance of a class gets a fresh
    copy of the state information, as a natural byproduct of Python's object model. Classes
    also support inheritance, multiple behaviors, and other tools.
    In classes, we save every attribute explicitly, whether it's changed or just referenced,
    and they are available outside the class. As for nested functions and nonlocal, the class
    alternative supports multiple copies of the retained data
    '''
    def __init__(self, start):                  # On object construction
        self.state = start                      # save state explicitly in new object
    def __call__(self, label):
        print(label, self.state)                # Reference state explicitly
        self.state += 1                         # Changes are always allowed


F = tester(0)                                   # Create instance, invoke __init__()
F('spam')                                # F is passed to self
F('ham')

G = tester(42)                                  # Each instance gets new copy of state
G('toast')                               # Changing one doesn't impact others
G('bacon')


F('eggs')
print('Final state is %s' % F.state)
