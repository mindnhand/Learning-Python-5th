#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------------
# Usage: python3 sumtree.py
# Description: why recursive function
#---------------------------------------------------------



'''
recursion--or equivalent explicit stack-based algorithms we'll meet
shortly--can be required to traverse arbitrarily shaped structures.

[1, [2, [3, 4], 5], 6, [7, 8]] # Arbitrarily nested sublists

Simple looping statements won't work here because this is not a linear iteration. Nested
looping statements do not suffice either, because the sublists may be nested to arbitrary
depth and in an arbitrary shape--there's no way to know how many nested loops to
code to handle all cases. Instead, the following code accommodates such general nesting
by using recursion to visit sublists along the way:
'''


def sumtree(seq):
    tot = 0
    for x in seq:                            # For each item at this level
        if not isinstance(x, list):
            tot += x                         # If x is not a list, add numbers directly
        else:
            tot += sumtree(x)                # If x is a list, recur for sumtree function call
    return tot




#-------------------------------test----------------------------------
seq_lst = [1, [2, [3, 4], 5], 6, [7, 8]]     # Arbitrary nesting structure
sum_res = sumtree(seq_lst)                   # sum_res is 36
print('The sum result of %s is %s' % (seq_lst, sum_res))


# Pathological cases
print(sumtree([1, [2, [3, [4, [5]]]]]))      # Prints 15 (right-heavy)
print(sumtree([[[[[1], 2], 3], 4], 5]))      # Prints 15 (left-heavy)
