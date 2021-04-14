#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 7-manage-instance-deco.py
# Description: class decorator to trace external instance attribute fetches
#---------------------------------------------


def tracer(klass):              # on @ decorator
    class Wrapper:
        def __init__(self, *args, **kwargs):            # on instance creation
            self.wrapped = klass(*args, **kwargs)       # use enclosing scope name
        
        def __getattr__(self, attrname):
            print('Trace: ', attrname)                  # catches all but .wrapped
            return getattr(self.wrapped, attrname)      # delegate to wrapped object
    return Wrapper


@tracer
class Person:                   # Person = tracer(Person)
    def __init__(self, name ,hours, rate):              # Wrapper remembers Person
        self.name = name
        self.hours = hours
        self.rate = rate        # in-method fetch not traced
    
    def pay(self):
        return self.hours * self.rate



if __name__ == '__main__':
    bob = Person('Bob', 40, 50)         # bob is really a Wrapper
    print(bob.name)                     # Wrapper embeds a Person
    print(bob.pay())                    # trigger __getattr__

