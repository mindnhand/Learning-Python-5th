#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 3-calltracer_descr-for-method.py
# Description: make descriptor class as decorator to decorate class method
#--------------------------------------------


class Tracer:       # a decorator + descriptor
    def __init__(self, func):       # on @ decorator
        print('in property descriptor __init__')
        self.calls = 0
        self.func = func
    def __get__(self, instance, owner):         # on method attribute fetch
        print('in property descriptor __get__')
        def wrapper(*args, **kwargs):           
            '''
            retain state information in both instance
            on method call: proxy with self+instance
            '''
            print('in enclosing method wrapper')
            self.calls += 1
            print('call %s to %s' % (self.calls, self.func.__name__))
            return self.func(instance, *args, **kwargs)      # runs __call__
        return wrapper



'''
# apply to normal function
@Tracer
def spam(a, b, c):
    print('in original function spam')
    print('<', a + b + c, '>')

@Tracer
def eggs(x, y):
    print('in original function eggs')
    print('<', x ** y, '>')

# fail to normal function
Chapter39.Decorators]# python3 3-calltracer_descr-for-method-2.py                                                                 
in property descriptor __init__
in property descriptor __init__
in property descriptor __init__
in property descriptor __init__

Entrance


Apply to simple function

Traceback (most recent call last):
      File "3-calltracer_descr-for-method-2.py", line 67, in <module>
          spam(1, 2, 3)
          TypeError: 'Tracer' object is not callable
'''

# apply to class method
class Person:
    def __init__(self, name, pay):
        print('in original class Person __init__')
        self.name = name
        self.pay = pay

    @Tracer
    def giveRaise(self, percent):
        print('in decorated class giveRaise method')
        self.pay *= (1.0 + percent)

    @Tracer
    def lastName(self):
        print('in decorated class lastName method')
        return self.name.split()[-1]



if __name__ == '__main__':
    print('\n\033[1;36mEntrance\033[0m\n')
    #print('\n\033[1;37mApply to simple function\033[0m\n')
    #spam(1, 2, 3)
    #spam(a=4, b=5, c=6)

    print('\n\033[1;37mApply to class method\033[0m\n')
    bob = Person('Bob Smith', 50000)
    sue = Person('Sue Jones', 100000)
    print('<', bob.name, sue.name, '>')
    sue.giveRaise(.10)
    print(int(sue.pay))
    print('<', bob.lastName(), sue.lastName(), '>')


    """
    Execution results:
    Chapter39.Decorators]# python3 3-calltracer_descr-for-method-2.py
    """
