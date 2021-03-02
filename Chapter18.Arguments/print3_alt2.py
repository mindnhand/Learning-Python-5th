#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: 
# Description: 
#--------------------------------------------



import sys


def print3(*args, **kargs):
    sep = kargs.pop('sep', ' ')
    end = kargs.pop('end', '\n')
    file = kargs.pop('file', sys.stdout)
    if kargs:
        raise TypeError('extra keywords: %s' % kargs)
    output = ''
    
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)



print3(99, (1, 2, 3), sep='@')
print3(909, name='bob')         # will raise an Exception
