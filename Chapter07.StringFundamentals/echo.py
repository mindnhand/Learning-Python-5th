#!/usr/bin/env python3
#encoding=utf-8



#--------------------------------
# Usage: python3 echo.py -a -b -c
#--------------------------------

import sys

print('argv: ', end=' ')
#print('argv: ')
print(sys.argv)

# print arguments without the script name 
output = 'arguments: %s' % sys.argv[1:]
print(output)
