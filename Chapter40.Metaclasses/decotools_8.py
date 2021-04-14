#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 decotools_8.py
# Description: assorted decorator tools
#-----------------------------------------------



import time


def tracer(func):               # use function, not class' __call__ method
    calls = 0                   # else self is decorator instance only
    def onCall(*args, **kwargs):
        nonlocal calls
        calls += 1
        print('call %s to %s' % (calls, func.__name__))
        return func(*args, **kwargs)
    return onCall


def timer(label='', trace=True):            # on decorator args: retain args
    def onDecorator(func):                  # on @ retain decorated func
        def onCall(*args, **kwargs):        # on calls: call original
            start = time.time()             # state is scopes + func attr
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            onCall.alltime += elapsed
            if trace:
                format = '%s%s: %.5f, %.5f'
                values = (label, func.__name__, elapsed, onCall.alltime)
                print(format % values)
            return result
        onCall.alltime = 0
        return onCall
    return onDecorator
