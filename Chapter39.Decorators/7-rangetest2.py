#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------
# Usage: python3 7-rangetest2.py
# Description: range test, it support position arguments, keyword arguments, default arguments
#------------------------------------


'''
The mutation of our example shown next does better. By matching the wrapped function's expected
arguments against the actual arguments passed in a call, it supports range validations for
arguments passed by either position or keyword name, and it skips testing for default arguments 
omitted in the call. In short, arguments to be validated are specified by keyword arguments to 
the decorator, which later steps through both the *pargs positionals tuple and the **kargs 
keywords dictionary to validate.

File rangetest.py: function decorator that performs range-test validation for arguments passed 
to any function or method.

Arguments are specified by keyword to the decorator. In the actual call, arguments may be passed 
by position or keyword, and defaults may be omitted. See rangetest_test.py for example use cases.
'''


trace = True

def rangetest(**args_check):            # Validate ranges for both+defaults
    def onDecorator(func):              # onCall remembers func and args_check
        if not __debug__:               # True if "python3 -O main.py args..."
            return func
        else:
            code = func.__code__
            allargs = code.co_varnames[:code.co_argcount]
            funcname = func.__name__
            def onCall(*args, **kwargs):
                '''
                All pargs match first N expected args by position
                The rest must be in kargs or be omitted defaults
                '''
                expected = list(allargs)
                positionals = expected[:len(args)]
                
                for (argname, (low, high)) in args_check.items():
                    # for all args to be checked
                    if argname in kwargs:
                        # argname was passed by name
                        if kwargs[argname] < low or kwargs[argname] > high:
                            errmsg = '{0} argument "{1}" not in {2}...{3}'
                            errmsg = errmsg.format(funcname, argname, low, high)
                            raise TypeError(errmsg)
                    elif argname in positionals:
                        # argname was passed by position
                        position = positionals.index(argname)
                        if args[position] < low or args[position] > high:
                            errmsg = '{0} argument "{1}" not in {2}...{3}'
                            errmsg = errmsg.format(funcname, argname, low, high)
                            raise TypeError(errmsg)
                    else:
                        # Assume argname was not passed: default
                        if trace:
                            print('Argument "{0}" defaulted'.format(argname))
                return func(*args, **kwargs)            # ok, run original call
            return onCall
    return onDecorator



if __name__ == '__main__':
    # test functions, positional and keyword
    @rangetest(age=(0, 120))            # persinfo = rangetest(...)(persinfo)
    def persinfo(name, age):
        print('%s is %s years old' % (name, age))

    @rangetest(M=(1, 12), D=(1, 31), Y=(0, 2021))
    def birthday(M, D, Y):
        print('birthday = {0}/{1}/{2}'.format(M, D, Y))

    persinfo('Bob', 40)
    persinfo(age=40, name='Bob')
    birthday(5, D=1, Y=1963)
    #persinfo('Bob', 150)
    #persinfo(age=150, name='Bob')
    #birthday(5, D=40, Y=1963)


    # Test methods, positional and keyword
    class Person:
        def __init__(self, name, job, pay):
            self.job = job
            self.pay = pay
        
        # giveRaise = rangetest(...)(giveRaise)
        @rangetest(percent=(0.0, 1.0))          # percent passed by position or name
        def giveRaise(self, percent):
            self.pay = int(self.pay * (1 + percent))

    bob = Person('Bob Smith', 'dev', 100000)
    sue = Person('Sue Jones', 'dev', 100000)
    bob.giveRaise(.10)
    sue.giveRaise(percent=.20)
    print(bob.pay, sue.pay)
    #bob.giveRaise(1.10)
    #bob.giveRaise(percent=1.20)

    # Test omitted defaults: skipped
    @rangetest(a=(1, 10), b=(1, 10), c=(1, 10), d=(1, 10))
    def omitargs(a, b=7, c=8, d=9):
        print(a, b, c, d)

    omitargs(1, 2, 3, 4)
    omitargs(1, 2, 3)
    omitargs(1, 2, 3, d=4)
    omitargs(1, d=4)
    omitargs(d=4, a=1)
    omitargs(1, b=2, d=4)
    omitargs(d=8, c=7, a=1)
    #omitargs(1, 2, 3, 11)              # Bad d
    #omitargs(1, 2, 11)                 # Bad c
    #omitargs(1, 2, 3, d=11)            # Bad d
    #omitargs(11, d=4)                  # Bad a
    #omitargs(d=4, a=11)                # Bad a
    #omitargs(1, b=11, d=4)             # Bad b
    #omitargs(d=8, c=7, a=11)           # Bad a
