#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 nested_default_lambda.py
# Description: nested scope and default argument
#------------------------------------------


# nested scope rules
def func():                             # it works because of the nested scope rules
    x = 4
    action = (lambda n: x ** n)         # x remembered from enclosing def
    return action


x = func()
print(x(2))                             # prints 16, 4 ** 2



# passing default argument
def func1():                            # it works because of the default value in argument passing
    x = 4
    action = (lambda n, x=x: x ** n)    # pass default argument x=x
    return action

x1 = func1()
print(x1(3))
