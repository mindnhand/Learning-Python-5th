#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 decoall-deco-any.py
# Description: class decorator factory: apply decorator to all methods of a class
#------------------------------------------------


from types import FunctionType
from decotools_8 import tracer, timer


'''
Notice that the class decorator returns the original, augmented class, not a wrapper layer
for it (as is common when wrapping instance objects instead). As for the metaclass version,
we retain the type of the original class -- an instance of Person is an instance of Person, 
not of some wrapper class. In fact, this class decorator deals with class creation only;
instance creation calls are not intercepted at all.

This distinction can matter in programs that require type testing for instances to yield the 
original class, not a wrapper. When augmenting a class instead of an instance, class decorators 
can retain the original class type. The class's methods are not their original functions because
they are rebound to decorators, but this is likely less important in practice, and it's true in 
the metaclass alternative as well.
'''

def decorateAll(decorator):
    def decoDecorate(klass):
        for attr, attrval in klass.__dict__.items():
            if type(attrval) is FunctionType:
                setattr(klass, attr, decorator(attrval))
        return klass
    return decoDecorate


# implementation 1:
@decorateAll(tracer)         # use a class decorator, decorate all with tracer
class Person1:                # applies func decorator to methods
    def __init__(self, name ,pay):          # Person = decorateAll(...)(Person)
        self.name = name                    # Person = decoDecorate(Person)
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]

# implementation 2:
@decorateAll(timer())           # decorate all with timer, defaults
class Person2:                # applies func decorator to methods
    def __init__(self, name ,pay):          # Person = decorateAll(...)(Person)
        self.name = name                    # Person = decoDecorate(Person)
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]

@decorateAll(timer(label='@@'))     # decorate all with timer, but pass a decorator argument
class Person3:                # applies func decorator to methods
    def __init__(self, name ,pay):          # Person = decorateAll(...)(Person)
        self.name = name                    # Person = decoDecorate(Person)
        self.pay = pay

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def lastName(self):
        return self.name.split()[-1]



if __name__ == '__main__':
    print('\033[1;34mImplementation 1\033[0m')
    bob1 = Person1('Bob Smith', 50000)
    sue1 = Person1('Sue Jones', 100000)
    print(bob1.name, sue1.name)
    sue1.giveRaise(.10)
    print('%.2f' % sue1.pay)
    print(bob1.lastName(), sue1.lastName())
    print()


    print('\033[1;34mImplementation 2\033[0m')
    bob2 = Person2('Bob Smith', 50000)
    sue2 = Person2('Sue Jones', 100000)
    print(bob2.name, sue2.name)
    sue2.giveRaise(.10)
    print('%.2f' % sue2.pay)
    print(bob2.lastName(), sue2.lastName())
    # If using timer: total time per method
    print('-'*40)
    print('%.5f' % Person2.__init__.alltime)
    print('%.5f' % Person2.giveRaise.alltime)
    print('%.5f' % Person2.lastName.alltime)
    print()


    print('\033[1;34mImplementation 3\033[0m')
    bob3 = Person3('Bob Smith', 50000)
    sue3 = Person3('Sue Jones', 100000)
    print(bob3.name, sue3.name)
    sue3.giveRaise(.10)
    print('%.2f' % sue3.pay)
    print(bob3.lastName(), sue3.lastName())
    # If using timer: total time per method
    print('-'*40)
    print('%.5f' % Person3.__init__.alltime)
    print('%.5f' % Person3.giveRaise.alltime)
    print('%.5f' % Person3.lastName.alltime)
    print()
