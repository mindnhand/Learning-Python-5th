#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------
# Usage: python3 factory_lambda.py
# Description: state retention with enclosing lambda
#----------------------------------------



def maker(n):                       # outside function, return anonymous function
    return lambda x: x ** n         # lambda, return x ** n

f2 = maker(2)                       # pass 2 to argument n, calculate the x ** 2
res2 = f2(3)                        # pass 3 to argument x, calculate the 3 ** 2
print('%s ** 2 = %s' % (3, res2))


f3 = maker(3)                       # pass 3 to argument n, calculate the x ** 3
res3 = f3(3)                        # pass 3 to argument x, calculate the 3 ** 3
print('%s ** 3 = %s' % (3, res3))

