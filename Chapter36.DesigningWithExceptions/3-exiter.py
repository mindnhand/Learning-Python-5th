#!/usr/bin/env python
#encoding=utf-8


#-----------------------------------------
# Usage: python3 3-exiter.py
# Description: scripts normally exit when control falls off the end of the top-level file. 
#              However, Python also provides a built-in sys.exit(statuscode) call to allow 
#              early terminations. This actually works by raising a built-in SystemExit 
#              exception to end the program, so that try/finally handlers run on the way out
#              and special types of programs can intercept the event. Because of this, a try
#              with an empty except might unknowingly prevent a crucial exit
#-----------------------------------------



import sys


def bye():
    sys.exit(0)         # Crucial error: abort now


try:
    bye()
except:
    print('got it')     # Oops -- we ignored the exit


print('continuing...')
