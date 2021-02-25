#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------
# Usage: python3 proper_indentation.py
# Description: if statement and indent
#-------------------------------------


x = 'SPAM'

if 'rubbery' in 'shrubbery':
    print(x * 8)
    x += 'NI'
    if x.endswith('NI'):
        x *= 2
        print(x)
