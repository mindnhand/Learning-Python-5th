#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------------
# Usage:
# Description: 
#-------------------------------------------------------



def func_anno(a: 'longth', b: 'width', h: 'height') -> 'cube volume':
    return a * b * h

def func_anno1(a: 'spam', b: (1, 10), c: float) -> int:
    return a + b + c

def func_anno2(a: 'spam', b, c: 99):
    return a + b + c

def func_anno3(a: 'spam' = 4, b: (1, 10) = 5, c: float = 6) -> int:
    '''
    First, you can still use defaults for arguments if you code annotations --
    the annotation (and its : character) appear before the default (and its = character). 
    In the following, for example, a: 'spam' = 4 means that argument
    a defaults to 4 and is annotated with the string 'spam':
    '''
    return a + b + c


#------------------------test-----------------------------
print('#<==test func_anno==>#')
cube_vol = func_anno(3, 4, 5)
print('the result of calling func_anno is %s' % cube_vol)
print('The function annotation of func_anno is %s' % func_anno.__annotations__)
print()


print('#<==test func_anno1==>#')
print('The function annotation of func_anno1 is %s' % func_anno1.__annotations__)
print()

print('#<==test func_anno2==>#')
print('The function annotation of func_anno2 is %s' % func_anno2.__annotations__)
print('key -> value relation in func_anno2 is following: ')
for arg in func_anno2.__annotations__:
    print('%s => %s' % (arg, func_anno2.__annotations__[arg]))
print()

print('#<==test func_anno3==>#')
default_argu_res = func_anno3()
print('the default result of func_anno3 is %s' % default_argu_res)
res = func_anno3(1, 2, 3)
print('the result of func_anno3(1, 2, 3) is %s' % res)
res1 = func_anno3(1, c=10)
print('the result of func_anno3(1, c=10) is %s' % res1)
print('The annotation of func_anno3 is %s' % func_anno3.__annotations__)
