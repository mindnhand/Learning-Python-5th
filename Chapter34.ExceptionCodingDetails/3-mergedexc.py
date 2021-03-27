#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 3-mergedexc.py
# Description: try - except - else - finally
#---------------------------------------------------





# File mergedexc.py (Python 3.X + 2.X)
sep = '-' * 45 + '\n'

print(sep + 'EXCEPTION RAISED AND CAUGHT')
try:
    x = 'spam'[99]
except IndexError:
    print('except run')
finally:
    print('finally run')

print('after run')
print()


print(sep + 'NO EXCEPTION RAISED')
try:
    x = 'spam'[3]
except IndexError:
    print('except run')
finally:
    print('finally run')

print('after run')
print()


print(sep + 'NO EXCEPTION RAISED, WITH ELSE')
try:
    x = 'spam'[3]
except IndexError:
    print('except run')
else:
    print('else run')
finally:
    print('finally run')

print('after run')
print()


print(sep + 'EXCEPTION RAISED BUT NOT CAUGHT')
try:
    x = 1 / 0
except IndexError:
    print('except run')
finally:
    print('finally run')

print('after run')
print()
