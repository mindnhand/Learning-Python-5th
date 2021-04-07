#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 timerdeco2_testseqs.py
# Description: client for timer decorator
#---------------------------------------------


import sys

from timerdeco2 import timer


force = list if sys.version_info[0] == 3 else lambda X: X


@timer(label='[ccc]==>')
def listcomp(n):
    return [x * 2 for x in range(n)]


@timer(label='[MMM]==>', trace=True)
def mapcall(n):
    return force(map(lambda x: x * 2, range(n)))


for func in listcomp, mapcall:
    result = func(5)
    func(50000)
    func(500000)
    func(1000000)
    print(result)
    print('allTime = %s\n' % func.alltime)

print('map v.s. comp = %s' % round(mapcall.alltime / listcomp.alltime, 3))
