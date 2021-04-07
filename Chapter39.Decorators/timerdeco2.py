#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 timerdeco2.py
# Description: Adding Decorator Arguments
#--------------------------------------------


import time


def timer(label='', trace=True):            # on decorator args: retain args
    class Timer:
        def __init__(self, func):           # on @: retain decorated func
            self.func = func
            self.alltime = 0
        def __call__(self, *args, **kwargs):    # on calls: call original function
            start = time.time()
            result = self.func(*args, **kwargs)
            elapsed = time.time() - start
            self.alltime += elapsed
            if trace:
                format = '%s %s: %.5f, %.5f'
                values = (label, self.func.__name__, elapsed, self.alltime)
                print(format % values)
            return result
    return Timer


