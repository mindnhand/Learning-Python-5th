#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------
# Usage: python3 lambda_expression_vs_def_statement.py
# Description: lambda expression
#-----------------------------------------------------



# lambda expression can be an element in the list
'''
The lambda expression is most useful as a shorthand for def, when you need to stuff
small pieces of executable code into places where statements are illegal syntactically.
The preceding code snippet, for example, builds up a list of three functions 
by embedding lambda expressions inside a list literal;
'''
lst = [
        lambda x: x ** 2,           # Inline function definition
        lambda x: x ** 3,
        lambda x: x ** 4            # A list of three callable functions
        ]


print('=' * 20 + 'test for lambda' + '=' * 20)
for f in lst:
    print(f(2))                     # will print 4, 8, 16

print(lst[0](3))                    # will print 9



# def statement can't be an element of list
'''
a def won’t work inside a list literal like thiss because it is a statement, 
not an expression. The equivalent def coding would require
temporary function names (which might clash with others) and function definitions
outside the context of intended use (which might be hundreds of lines away):
'''

def f1(x): return x ** 2            # Define named functions
def f2(x): return x ** 3
def f3(x): return x ** 4


lst_def = [f1, f2, f3]              # Reference by name

print('=' * 20 + 'test for def' + '=' * 20)
for f in lst_def:
    print(f(2))                     # will print 4, 8 16

print(lst_def[0](3))
