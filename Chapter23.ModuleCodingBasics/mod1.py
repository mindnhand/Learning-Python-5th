#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 mod1.py
# Description: module basic
#-------------------------------------------
x = 1

import mod2

print(x, end=' ')           # my global x
print(mod2.x, end=' ')      # mod2's x
print(mod2.mod3.x)          # nested mod3's x
