#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 timer2.py
# Description: timer for total, bestof, bestoftotal
#-------------------------------------------------




"""
total(spam, 1, 2, a=3, b=4, _reps=1000) calls and times spam(1, 2, a=3, b=4)
_reps times, and returns total time for all runs, with final result.
bestof(spam, 1, 2, a=3, b=4, _reps=5) runs best-of-N timer to attempt to
filter out system load variation, and returns best time among _reps tests.
bestoftotal(spam 1, 2, a=3, b=4, _rep1=5, reps=1000) runs best-of-totals
test, which takes the best among _reps1 runs of (the total of _reps runs);
"""


import time, sys

timer = time.clock if sys.platform[:3] == 'win' else time.time

def total(func, *args, **kargs):
    _reps = kargs.pop('_reps', 1000)                            # Passed-in or default reps
    repslist = list(range(_reps))                               # Hoist range out for 2.x lists
    start = timer()
    for i in repslist:
        ret = func(*args, **kargs)
    elapsed = timer() - start
    return (elapsed, ret)


def bestof(func, *args, **kargs):
    _reps = kargs.pop('_reps', 5)
    best = 2 ** 32
    for i in range(_reps):
        start = timer()
        ret = func(*args, **kargs)
        elapsed = timer() - start
        best = elapsed if elapsed < best else best
    return (best, ret)


def bestoftotal(func, *args, **kargs):
    _reps1 = kargs.pop('_reps1', 5)
    return min(total(func, *args, **kargs) for i in range(_reps1))
