#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 6-access1.py
# Description: decorator implement private attribute
#-------------------------------------------


"""
File access1.py (3.X + 2.X)
Privacy for attributes fetched from class instances.
See self-test code at end of file for a usage example.
Decorator same as: Doubler = Private('data', 'size')(Doubler).
Private returns onDecorator, onDecorator returns onInstance,
and each onInstance instance embeds a Doubler instance.
"""


traceMe = False

def trace(*args):
    if traceMe:
        print('[' + ' '.join(map(str, args)) + ']')


def private(*privates):             # private in enclosing scope
    '''
    The class decorator used here accepts any number of arguments, to name private
    attributes. What really happens, though, is that the arguments are passed to 
    the private function, and private returns the decorator function to be applied 
    to the subject class. That is, the arguments are used before decoration ever 
    occurs; private returns the decorator, which in turn remembers the privates 
    list as an enclosing scope reference.

    Speaking of enclosing scopes, there are actually three levels of state retention
    at work in this code:
    - The arguments to private are used before decoration occurs and are retained as 
      an enclosing scope reference for use in both onDecorator and OnInstance.
    - The class argument to onDecorator is used at decoration time and is retained as 
      an enclosing scope reference for use at instance construction time.
    - The wrapped instance object is retained as an instance attribute in the OnInstance 
      proxy object, for use when attributes are later accessed from outside the class.
      This all works fairly naturally, given Python's scope and namespace rules.
    '''
    def onDecorator(aClass):        # aClass in enclosing scope
        class OnInstance:           # wrapped in instance attribute
            def __init__(self, *args, **kwargs):
                self.wrapped = aClass(*args, **kwargs)
            def __getattr__(self, attr):            # my attrs don't call getattr
                trace('get: ', attr)                # others assumed in wrapped
                if attr in privates:
                    raise TypeError('private attribute fetch ' + attr)
                else:
                    return getattr(self.wrapped, attr)
            def __setattr__(self, attr, value):     # outside attribute access
                trace('set: ', attr, value)         # others run normally
                if attr == 'wrapped':               # allow my attrs
                    self.__dict__[attr] = value     # avoid loop
                elif attr in privates:
                    raise TypeError('private attribute change ' + attr)
                else:
                    setattr(self.wrapped, attr, value)          # wrapped obj attrs
        return OnInstance
    return onDecorator          # private returns the decorator, which in turn remembers the privates list as an enclosing scope reference.


@private('data', 'size')            # Doubler = private(...)(Doubler)
class Doubler:
    def __init__(self, label, start):
        self.label = label          # access inside the subject class
        self.data = start           # not intercepted: run normally
    def size(self):
        return len(self.data)       # methods run without checking
    def double(self):               # because privacy not inherited
        for i in range(self.size()):
            self.data[i] = self.data[i] * 2
    def display(self):
        print('%s => %s' % (self.label, self.data))


if __name__ == '__main__':
    traceMe = True
    x = Doubler('x is ', [1, 2, 3])
    y = Doubler('y is ', [-10, -20, -30])

    # the following all successed
    print(x.label)                  # access outside subject class
    x.display(); x.double(); x.display()        # Intercepted: validated, delegated

    print(y.label)
    y.display(); y.double()
    y.label = 'Spam'
    y.display()


    # the following all failed
    '''
    print(x.size())                 # prints TypeError: private attribute fetch: size
    print(x.data)
    x.data = [1, 1, 1]
    x.size = lambda S: 0
    print(y.data)
    print(y.size()) 
    '''
