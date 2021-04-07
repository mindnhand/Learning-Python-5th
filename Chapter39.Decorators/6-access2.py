#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 6-access2.py
# Description: class decorator with private and public attribute declaration
#---------------------------------------------


'''
File 6-access2.py (3.X + 2.X)
Class decorator with Private and Public attribute declarations.
Controls external access to attributes stored on an instance, or
Inherited by it from its classes. Private declares attribute names
that cannot be fetched or assigned outside the decorated class,
and Public declares all the names that can.
Caveat: this works in 3.X for explicitly named attributes only: __X__
operator overloading methods implicitly run for built-in operations
do not trigger either __getattr__ or __getattribute__ in new-style
classes. Add __X__ methods here to intercept and delegate built-ins.

Again, study this code on your own to get a feel for how this works. Notice that
this scheme adds an additional fourth level of state retention at the top, beyond 
that described in the preceding section: the test functions used by the lambdas 
are saved in an extra enclosing scope. This example is coded to run under either 
Python 3.X or 2.X (2.6 or later), though it comes with a caveat when run under 3.X
(explained briefly in the file's docstring and expanded on after the code)
'''


traceMe = False

def trace(*args):
    if traceMe:
        print('[' + ' '.join(map(str, args)) + ']')


def accessControl(failIf):
    def onDecorator(aClass):
        class OnInstance:
            def __init__(self, *args, **kwargs):
                self.__wrapped = aClass(*args, **kwargs)
            def __getattr__(self, attr):
                trace('get: ', attr)
                if failIf(attr):
                    raise TypeError('private attribute fetch: ' + attr)
                else:
                    return getattr(self.__wrapped, attr)
            def __setattr__(self, attr, value):
                trace('set: ', attr, value)
                if attr == '_OnInstance__wrapped':
                    self.__dict__[attr] = value
                elif failIf(attr):
                    raise TypeError('private attribute change: ' + attr)
                else:
                    setattr(self.__wrapped, attr, value)
        return OnInstance
    return onDecorator


def private(*attributes):
    return accessControl(failIf=lambda attr: attr in attributes)

def public(*attributes):
    return accessControl(failIf=lambda attr: attr not in attributes)



if __name__ == '__main__':
    @private('age')             # Person = private('age')(Person)
    class PriPerson:               # Person = OnInstance with state
        def __init__(self, name, age):
            self.name = name
            self.age = age      # inside access run normally

    x = PriPerson('Bob', 40)
    print(x.name)               # outside access valided

    x.name = 'Sue'
    print(x.name)

    '''
    # print(x.age)              # this will incur exception
    Chapter39.Decorators]# python3 6-access2.py
    Bob
    Sue
    Traceback (most recent call last):
      File "6-access2.py", line 82, in <module>
        print(x.age)
      File "6-access2.py", line 47, in __getattr__
        raise TypeError('private attribute fetch: ' + attr)
    TypeError: private attribute fetch: age
    '''

    @public('name')
    class PubPerson:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    y = PubPerson('Bob', 40)
    print(y.name)
    y.name = 'Sue'
    print(y.name)

    '''
    # print(x.age)
    # x.age = 50
    Chapter39.Decorators]# python3 6-access2.py
    Bob
    Sue
    Bob
    Sue
    Traceback (most recent call last):
      File "6-access2.py", line 107, in <module>
        print(x.age)
      File "6-access2.py", line 47, in __getattr__
        raise TypeError('private attribute fetch: ' + attr)
    TypeError: private attribute fetch: age
    '''
