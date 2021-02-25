#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------
# Usage: python3 break_else.py
# Description: find prime
#-----------------------------



y = int(input('Enter an integer: '))

x = y // 2

while x > 1:
    if y % x == 0:
        print('%s has factor %s' % (y, x))
        break
    x -= 1
else:
    print('%s is prime' % y)
