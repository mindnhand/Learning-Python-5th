#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 7-manage-instance-meta.py
# Description: manage instance with metaclass
#-----------------------------------------------


def tracer(classname, supers, classdict):               # on class creation call
    klass = type(classname, supers, classdict)          # make client class
    class Wrapper:
        def __init__(self, *args, **kwargs):            # on instance creation
            self.wrapped = klass(*args, **kwargs)

        def __getattr__(self, attrname):
            print('Trace: ', attrname)                  # catch all but .wrapped
            return getattr(self.wrapped, attrname)      # delegate to wrapped object
    return Wrapper


class Person(metaclass=tracer):                         # make person with tracer metaclass
    def __init__(self, name ,hours, rate):               # wrapper members Person
        self.name = name
        self.hours = hours
        self.rate = rate

    def pay(self):
        return self.hours * self.rate



if __name__ == '__main__':
    bob = Person('Bob', 40, 50)                         # bob is reality a Wrapper
    print(bob.name)                                     # Wrapper embeds a Person
    print(bob.pay())                                      # Triggers __getattr__
