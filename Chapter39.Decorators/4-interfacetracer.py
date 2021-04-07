#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 4-interfacetracer.py
# Description: trace interfaces with class decorator
#---------------------------------------------



# the original nondecorator delegation
class WrapperNonDeco:
    '''
    >>> x = Wrapper([1,2,3])          # Wrap a list
    >>> x.append(4)                   # Delegate to list method
    Trace: append
    >>> x.wrapped                     # Print my member
    [1, 2, 3, 4]
    >>> x = Wrapper({"a": 1, "b": 2}) # Wrap a dictionary
    >>> list(x.keys())                # Delegate to dictionary method
    Trace: keys                       # Use list() in 3.X
    ['a', 'b']
    '''
    def __init__(self, object):
        self.wrapped = object
    def __getattr__(self, attrname):
        print('Trace: ', attrname)              # Trace fetch
        return getattr(self.wrapped, attrname)  # Delegation fetch
    '''
    In this code, the Wrapper class intercepts access to any of the wrapped 
    object's named attributes, prints a trace message, and uses the getattr
    built-in to pass off the request to the wrapped object. Specifically, it
    traces attribute accesses made outside the wrapped object's class; accesses
    inside the wrapped object's methods are not caught and run normally by design. 
    This whole-interface model differs from the behavior of function decorators,
    which wrap up just one specific method.
    '''

# Class decorators provide an alternative and convenient way to code this __getattr__ technique to wrap an entire interface.
def tracer(aClass):         # on @ decoration
    class Wrapper:
        def __init__(self, *args, **kwargs):        # on instance creation
            self.fetches = 0
            self.warpped = aClass(*args, **kwargs)  # use enclosing scope name

        def __getattr__(self, attrname):
            print('Trace: ' + attrname)             # catch all but own attrs
            self.fetches += 1
            # return getattr(self.wrapped, attrname)  # delegate to wrapped object, this will trigger loop
            return object.__getattribute__(self.wrapped, attrname)      # also trigger loop, but in python3.6 works
            '''
            Trace: wrapped
            Trace: wrapped
            Trace: wrapped
            Trace: wrapped
            Trace: wrapped
            Traceback (most recent call last):
	    File "4-interfacetracer.py", line 74, in <module>
	      food.display()                  # Triggers __getattr__
	    File "4-interfacetracer.py", line 51, in __getattr__
	      return object.__getattribute__(self.wrapped, attrname)
	    File "4-interfacetracer.py", line 51, in __getattr__
	      return object.__getattribute__(self.wrapped, attrname)
	    File "4-interfacetracer.py", line 51, in __getattr__
	      return object.__getattribute__(self.wrapped, attrname)
	    [Previous line repeated 992 more times]
	    File "4-interfacetracer.py", line 48, in __getattr__
	      print('Trace: ' + attrname)             # catch all but own attrs
            '''
    return Wrapper


@tracer
class Spam:                     # Spam = tracer(Spam) => Wrapper
    def display(self):          # Spam is rebound to Wrapper
        print('Spam!' * 8)

@tracer
class Person:
    def __init__(self, name, hours, rate):      # Wrapper remembers Person
        self.name = name
        self.hours = hours
        self.rate = rate
    def pay(self):              # access outside class traced
        return self.hours * self.rate       # in-method accesses not traced




if __name__ == '__main__':
    food = Spam()                   # Triggers Wrapper()
    food.display()                  # Triggers __getattr__
    #print([food.fetches])

    '''
    bob = Person('Bob', 40, 50)     # bob is really a Wrapper
    print(bob.name)                 # Wrapper embeds a Person
    print(bob.pay())
    print('')

    sue = Person('sue', rate=100, hours=60)     # sue is a different Wrapper
    print(sue.name)                 # with a different person
    print(sue.pay())
    print(bob.name)                 # bob has different state
    print(bob.pay())
    print([bob.fetches, sue.fetches])       # Wrapper attrs not traced
    '''
