#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 3-calltracer-for-method.py
# Description: enclosing scope and nonlocal to decorate method
#--------------------------------------------



def tracer(func):               # Use function, not class with __class__ builtin
    calls = 0
    def onCall(*args, **kwargs):           # Else "self" is decorator instance only
        nonlocal calls
        calls += 1
        print('call %s to %s' % (calls, func.__name__))
        return func(*args, **kwargs)
    return onCall



# apply to simple function
@tracer
def spam(a, b, c):
    print(a + b + c)

@tracer
def eggs(x, y):
    print(x ** y)


# apply to class method
class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    @tracer
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    @tracer
    def lastName(self):
        return self.name.split()[-1]




if __name__ == '__main__':
    print('\033[1;37mApply to simple function\033[0m')
    spam(1, 2, 3)
    spam(a=4, b=5, c=6)

    print('\n\033[1;37mApply to class method\033[0m')
    bob = Person('Bob Smith', 50000)
    sue = Person('Sue Jones', 100000)
    print(bob.name, sue.name)
    sue.giveRaise(.10)
    print(int(sue.pay))
    print(bob.lastName(), sue.lastName())
