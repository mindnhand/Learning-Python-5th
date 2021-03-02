#!/usr/bin/env python3
#encoding=utf-8



#----------------------------------------------
# Usage: keyword_only_arguments.py
# Description: example for keyword-only-arguments
#              also named print3_alt1.py
#----------------------------------------------



import sys



def print3(*args, sep=' ', end='\n', file=sys.stdout):
    output = ''
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)


print3(99, 'string', sep='@')
print3(99, (1, 2, 3), name='bob')       # will raise an Exception
'''
# python3 keyword_only_arguments.py
99@string
Traceback (most recent call last):
      File "keyword_only_arguments.py", line 28, in <module>
          print3(99, (1, 2, 3), name='bob')
          TypeError: print3() got an unexpected keyword argument 'name'
'''
