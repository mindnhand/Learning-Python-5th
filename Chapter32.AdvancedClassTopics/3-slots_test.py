#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------
# Usage: python3 slots_test.py
# Description: 
#-----------------------------------



"""
In [165]: import timeit
In [166]: base = '''
     ...: Is = []
     ...: for i in range(1000):
     ...:     x = C()
     ...:     x.a = 1; x.b = 2; x.c = 3; x.d =4
     ...:     t = x.a + x.b + x.c + x.d
     ...:     Is.append(x)
     ...: '''

In [167]: stmt = '''
     ...: class C:
     ...:     __slots__ = ['a', 'b', 'c', 'd']
     ...: ''' + base

In [168]: print(min(timeit.repeat(stmt=stmt, number=1000, repeat=3)))
0.6733840969391167

In [169]: stmt1 = '''
     ...: class C:
     ...:     pass
     ...: ''' + base

In [170]: 

In [170]: print(min(timeit.repeat(stmt=stmt1, number=1000, repeat=3)))
0.8323119629640132Z
"""


import timeit
base = '''
Is = []
for i in range(1000):
    x = C()
    x.a = 1; x.b = 2; x.c = 3; x.d =4
    t = x.a + x.b + x.c + x.d
    Is.append(x)
'''

stmt = '''
class C:
    __slots__ = ['a', 'b', 'c', 'd']
''' + base

print('Slots => ', end=' ')
print(min(timeit.repeat(stmt=stmt, number=1000, repeat=3)))

stmt1 = '''
class C:
    pass
''' + base

print('NonSlots => ', end=' ')
print(min(timeit.repeat(stmt=stmt1, number=1000, repeat=3)))


'''
Output:
Slots =>  0.6635029220487922
NonSlots =>  0.8341730549000204
'''
