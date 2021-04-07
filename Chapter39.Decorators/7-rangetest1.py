#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 7-rangetest1.py
# Description: range-test decorator
#--------------------------------------------



def rangetest(*args_check):               # validate positional arguments ranges
    def onDecorator(func):
        if not __debug__:           # True if "python3 -O main.py args..."
            return func
        else:
            def onCall(*args):
                for (ix, low, high) in args_check:
                    if args[ix] < low or args[ix] > high:
                        errmsg = 'Argument %s not in %s...%s' % (ix, low, high)
                        raise TypeError(errmsg)
                return func(*args)
            return onCall
    return onDecorator



if __name__ == '__main__':
    print(__debug__)                    # False if python -O main.py

    @rangetest((1, 0, 120))             # persinfo = rangetest(...)(persinfo)
    def persinfo(name, age):            # age must be in 0..120
        print('%s is %s years old' % (name, age))

    @rangetest([0, 1, 12], [1, 1, 31], [2, 0, 2009])
    def birthday(M, D, Y):
        print('birthday = {0}/{1}/{2}'.format(M, D, Y))

    class Person:
        def __init__(self, name, job, pay):
            self.job = job
            self.pay = pay

        @rangetest([1, 0.0, 1.0])       # giveRaise = rangetest(...)(giveRaise)
        def giveRaise(self, percent):   # arg 0 is the self instance here
            self.pay = int(self.pay * (1 + percent))

    # Comment lines raise TypeError unless "python -O" used on shell command line
    persinfo('Bob Smith', 45)           # really run onCall(...) with state
    # persinfo('Bob Smith', 200)        # python -O can run this line

    birthday(5, 31, 1963)
    # birthday(5, 32, 1963)

    sue = Person('Sue Jones', 'dev', 100000)
    sue.giveRaise(.10)                  # really run onCall(self, .10)
    print(sue.pay)                      # or giveRaise(self, .10) if -O
    # sue.giveRaise(1.10)
    # print(sue.pay)

