#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------
# Usage: python3 5-tracer1.py
# Description: Recall from Chapter 30 that the __call__ operator overloading
#              method implements a function-call interface for class instances. 
#              The following code uses this to define a call proxy class that 
#              saves the decorated function in the instance and catches calls 
#              to the original name. Because this is a class, it also has state 
#              information -- a counter of calls made
#---------------------------------------


class Tracer:
    def __init__(self, func):               # Remember original, init counter
        self.calls = 0
        self.func = func

    def __call__(self, *args):              # On later calls: add logic, run original
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args)




if __name__ == '__main__':
    '''
    Because the spam function is run through the tracer decorator, when the original
    spam name is called it actually triggers the __call__ method in the class. This
    method counts and logs the call, and then dispatches it to the original wrapped 
    function. Note how the *name argument syntax is used to pack and unpack the passed-in
    arguments; because of this, this decorator can be used to wrap any function with
    any number of positional arguments.
    '''
    @Tracer                         # same as spam = Tracer(spam)
    def spam(a, b, c):              # Wrap spam in a decorator object
        return a + b + c

    print(spam(1, 2, 3))            # really call the Tracer wrapper object
    print(spam('a', 'b', 'c'))      # Invokes __call__ in class

    '''
    results:
    Chapter32.AdvancedClassTopics]# python3 5-tracer1.py
    call 1 to spam
    6
    call 2 to spam
    abc
    '''
