#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 functional_programming_tools.py
# Description: Functional Programming Tools
#---------------------------------------------



# 1. map 
'''
The map function applies a passed-in function to each item
in an iterable object and returns a list containing all the function call results.
'''

def inc(x): return x + 10

print('=' * 20 + 'test map' + '=' * 20)
counter = [1, 2, 3, 4]

updated = map(inc, counter)
print('updated result is %s' % list(updated))

updated_lambda = map(lambda x: x + 10, counter)
print('updated result of lambda is %s' % list(updated_lambda))


def mymap(func, seq):
    res = []
    for x in seq:
        res.append(func(x))
    return res

updated_mymap = mymap(inc, counter)                         # equal to [inc(x) for x in counter]
print('updated result of mymap is %s' % list(updated_mymap))

counter_1 = [5, 6, 7, 8]
updated_multi_seq = map(pow, counter, counter_1)            # equal to [pow(x, y) for x, y in zip(counter, counter_1)]
'''
the pow function takes two arguments on each call--one from each sequence passed  to map.
'''
print('updated result of multi_seq of pow is %s' % list(updated_multi_seq))




# 2. filter
'''
filter and reduce, select an iterable's items based on 
a test function and apply functions to item pairs, respectively.
'''
integers_lst = list(range(-5, 5))
greater0_lst = list(filter(lambda x: x > 0, integers_lst))

print('=' * 20 + 'test filter' + '=' * 20)
print('greater zero: %s' % greater0_lst)

greater0_lst_for = []
for x in integers_lst:
    if x > 0:
        greater0_lst_for.append(x)

print('greater zero for: %s' % greater0_lst_for)


lst_comprehension = [x for x in integers_lst if x > 0]
print('greater zero list comprehension: %s' % lst_comprehension)




# 3. functools.reduce
from functools import reduce
reduce_sum = reduce(lambda x, y: x + y, range(1, 5))         # equal to [x + list(range(1, 5))[0] for x in list(range(1, 5))[1:]]

print('=' * 20 + 'test functools.reduce' + '=' * 20)
print('the sum of range(1, 5) is %s' % reduce_sum)

reduce_multiply = reduce(lambda x, y: x * y, range(1, 5))
print('the multiply of range(1, 5) is %s' % reduce_multiply)

def myreduce(func, seq):
    tally = seq[0]
    for x in seq[1:]:
        tally = func(tally, x)
    return tally


myreduce_multiply = myreduce(lambda x, y: x * y, range(1, 5))
print('the multiply of range(1, 5) with myreduce is %s' % myreduce_multiply)


import operator
operator_mul = reduce(operator.mul, range(1, 5))
print('the multiply of range(1, 5) with operator.mul is %s' % operator_mul)
