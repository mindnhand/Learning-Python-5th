#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 1-kaboom.py
# Description: try-except don't terminate your program
#-----------------------------------------


def kaboom(x, y):
    print(x + y)                # Trigger TypeError


try:
    kaboom([0, 1, 2], 'spam')
except TypeError:               # Catch and recover here
    print('Hello World!')

print('Resume here')
