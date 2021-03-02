#!/usr/bin/env python3
#encoding=utf-8



#----------------------------------------------------------
# Usage: python3 tracer0.py
# Description: 
#----------------------------------------------------------



'''
In a function call, arguments must appear in this order: any positional arguments
(value); followed by a combination of any keyword arguments (name=value) and
the *iterable form; followed by the **dict form.
In a function header, arguments must appear in this order: any normal arguments
(name); followed by any default arguments (name=value); followed by the *name (or
* in 3.X) form; followed by any name or name=value keyword-only arguments (in
3.X); followed by the **name form.
In both the call and header, the **args form must appear last if present.

ABOUT function annotation
In Python 3.X only, argument names in a function header can also have
annotation values, specified as name:value (or name:value=default when
defaults are present). This is simply additional syntax for arguments and
does not augment or change the argument-ordering rules described here. 
The function itself can also have an annotation value, given as def f()->value. 
Python attaches annotation values to the function object.
See the discussion of function annotation in Chapter 19 for more details.
'''



def tracer(func, *args, **kwargs):                          # Accept arbitrary arguments
    print('calling: ', func.__name__)
    print('arguments: ', args, kwargs)
    return func(*args, **kwargs)                            # Pass along arbitrary arguments

def func(a, b, c, d):
    return a + b + c + d

print('call with key=value')
print(tracer(func, 1, 2, c=3, d=4))

t = (5, 6)
d = dict(c=7, d=8)
print('call with tuple and dict')
print(tracer(func, *t, **d))
