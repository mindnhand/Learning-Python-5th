#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 2-badly.py
# Description: traceback module to display exceptions
#--------------------------------------------



'''
the exception traceback object available in the prior section's sys.exc_info
result is also used by the standard library's traceback module to generate 
the standard error message and stack display manually. This file has a handful 
of interfaces that support wide customization, which we don't have space to
cover usefully here, but the basics are simple
'''


import traceback

def inverse(x):
    return 1 / x

try:
    inverse(0)
except Exception:
    traceback.print_exc(file=open('badly.exc', 'w'))


print('Bye')
