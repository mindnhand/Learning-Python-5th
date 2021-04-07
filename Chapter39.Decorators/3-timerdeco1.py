#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 3-timerdeco1.py
# Description: timing function decorators
#-----------------------------------------------


import sys
import time


force = list if sys.version_info[0] == 3 else lambda X: X

class Timer:
    def __init__(self, func):
        self.func = func
        self.alltime = 0
    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        elapsed = time.time() - start
        self.alltime += elapsed
        print('%s: %.5f, %.5f' % (self.func.__name__, elapsed, self.alltime))
        return result



@Timer
def listcomp(n):
    return [x * 2 for x in range(n)]


@Timer
def mapcall(n):
    return force(map((lambda x: x * 2), range(n)))



if __name__ == '__main__':
    print('\n\033[1;35mEntrance\033[0m\n')
    print('\033[1;37mlistcomp function\033[0m')
    result = listcomp(5)
    listcomp(50000)
    listcomp(500000)
    listcomp(1000000)
    print(result)
    print('allTime = %s' % listcomp.alltime)
    print('\n')
    
    print('\033[1;37mmapcall function\033[0m')
    result = mapcall(5)
    mapcall(50000)
    mapcall(500000)
    mapcall(1000000)
    print(result)
    print('allTime = %s' % mapcall.alltime)
    print('\nmapcall = %s' % round(mapcall.alltime / listcomp.alltime, 3))
