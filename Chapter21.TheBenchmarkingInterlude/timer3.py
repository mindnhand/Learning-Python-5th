#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------
# Usage: python3 timer3.py
# Description: timer function with keywordonly argument
#-----------------------------------------------------



'''
Same usage as timer2.py, but uses 3.X keyword-only default arguments
instead of dict pops for simpler code. No need to hoist range() out
of tests in 3.X: always a generator in 3.X, and this can't run on 2.X.
Keywordonly arguments are ideal for configuration options such as our 
functions' _reps argument. They must be coded after a * and before a ** 
in the function header, and in a function call they must be passed by 
keyword and appear before the ** if used. The following is a 
keyword-only-based alternative to the prior module.
'''


import time, sys


timer = time.clock if sys.platform[:3] == 'win' else time.time

'''
This module can be tested by timeseqs_timer2.py
'''
def total(func, *args, _reps=1000, **kargs):
    start = timer()
    for i in range(_reps):
        ret = func(*args, **kargs)
    elapsed = timer() - start
    return (elapsed, ret)


def bestof(func, *args, _reps=5, **kargs):
    best = 2 ** 32
    for i in range(_reps):
        start = timer()
        ret = func(*args, **kargs)
        elapsed = timer() - start
        best = elapsed if elapsed < best else best
    return (best, ret)


def bestoftotal(func, *args, _reps1=5, **kargs):
    return min(total(func, *args, **kargs) for i in range(_reps1))

