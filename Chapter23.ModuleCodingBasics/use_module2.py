#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------
# Usage: python3 use_module2.py
# Description: module basic
#------------------------------------------------------


import module2


print(module2.sys)
print(module2.name)
print(module2.klass)

print('The dict of module2 is: ')
print(list(module2.__dict__.keys()))

print('The dict of module2 without __xxx__ is: ')
print([x for x in module2.__dict__.keys() if not x.startswith('__')])
