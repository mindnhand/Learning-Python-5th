#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 factory_function.py
# Description: state retention with enclosing function
#-----------------------------------------



def maker(n):
    def action(x):          # make and return action
        return x ** n       # action retains n from maker, enclosing scope
    return action


f2 = maker(2)               # pass 2 to argument n, calculate the x ** 2
res2 = f2(3)                # pass 3 to x, x remembers 2; equal to 3 ** 2 = 9
print('%s ** 2 is %s' % (3, res2))       # prints 9


f3 = maker(3)               # pass 3 to argument n, calculate the x ** 3
res3 = f3(3)                # pass 3 to x, x remembers 3; equal to 3 ** 3 = 27
print('%s ** 3 is %s' % (3, res3))       # prints 27
