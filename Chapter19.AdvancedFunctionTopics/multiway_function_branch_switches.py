#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 multiway_function_branch_switches.py
# Description: lambda expression
#-------------------------------------------



# lambda
'''
Indexing by key fetches one of those functions, 
and parentheses force the fetched function to be called. When coded
this way, a dictionary becomes a more general multiway branching tool
'''
dict_lambda = {
        'already': (lambda: 2 + 2),
        'got': lambda: 2 + 4,
        'one': lambda: 2 ** 6
        }

print('=' * 20 + 'test for lambda' + '=' * 20)
for key in dict_lambda:
    print('the value of %s is %s' % (key, dict_lambda[key]()))


# def
def f1(): return 2 + 2
def f2(): return 2 + 4
def f3(): return 2 ** 6

dict_def = {
        'already': f1,
        'got': f2,
        'one': f3
        }

print('=' * 20 + 'test for def' + '=' * 20)
for key in dict_def:
    print('the value of %s is %s' % (key, dict_def[key]()))
