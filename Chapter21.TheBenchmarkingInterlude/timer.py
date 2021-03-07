#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 timer.py
# Description: usage of time module
#-----------------------------------------------




'''
Homegrown timing tools for function calls.
Does total time, best-of time, and best-of-totals time
'''

import time, sys


timer = time.clock if sys.platform[:3] == 'win' else time.time          # 如果是windows系统，则调用time.clock，如果是Linux系统，则调用time.time

def total(reps, func, *args, **kargs):
    '''
    Total time to run func() reps times.
    Returns (total time, last result)
    '''
    repslist = list(range(reps))
    start = timer()                                                     # Or time.perf_counter/other in 3.3+
    for i in repslist:
        ret = func(*args, **kargs)
    elapsed = timer() - start
    return (elapsed, ret)


def bestof(reps, func, *args, **kargs):
    '''
    Quickest func() among reps runs.
    Returns (best time, last result)
    '''
    best = 2 ** 32                                          # 136 years seems large enough
    for i in range(reps):                                   # range usage not time here
        start = timer()
        ret = func(*args, **kargs)
        elapsed = timer() - start                           # Or call total() with reps=1
        best = elapsed if elapsed < best else best          # Or add to list and take min()
    return (best, ret)


def bestoftotal(reps1, reps2, func, *args, **kargs):
    '''
    Best of totals:
    (best of reps1 runs of (total of reps2 runs of func))
    '''
    return bestof(reps1, total, reps2, func, *args, **kargs)



t1 = total(1000, pow, 2, 1000)[0]                # Compare to timer0 result above
t2 = total(1000, str.upper, 'spam')              # return (time, last call's result)
print(t1)
print(t2)
#print('total time of t1 = {}' % str(t1))
#print('total time of t2 = {}' % str(t2))

tb1 = bestof(1000, str.upper, 'spam')             # 1/1000 as long as total time
tb2 = bestof(1000, pow, 2, 1000000)[0]
print('bestof time of tb1 = %s' % str(tb1))
print('bestof time of tb2 = %s' % str(tb2))

tb3 = bestof(50, total, 1000, str.upper, 'spam')
tbt2 = bestoftotal(50, 1000, str.upper, 'spam')
print('bestof time of tb3 = %s' % str(tb3))
print('bestoftotal time of tbt2 = %s' % str(tbt2))
