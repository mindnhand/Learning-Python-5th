#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 generator_function.py
# Description: Generator Function
#------------------------------------------------



'''
The chief code difference between generator and normal functions is that a generator
yields a value, rather than returning one--the yield statement suspends the function
and sends a value back to the caller, but retains enough state to enable the function to
resume from where it left off. When resumed, the function continues execution 
immediately after the last yield run. From the function's perspective, this allows its 
code to produce a series of values over time, rather than computing them all at once and
sending them back in something like a list.
'''
def genesquares(num):
    for i in range(num):
        yield i ** 2


for i in genesquares(5):
    print(i, end=':')
else:
    print()
