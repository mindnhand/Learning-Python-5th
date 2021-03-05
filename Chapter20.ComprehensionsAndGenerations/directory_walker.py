#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------------
# Usage: python3 directory_walker.py
# Description: os.walk is a generator
#---------------------------------------------------------



import os


'''
the standard directory walker which at each level of a tree yields
a tuple of the current directory, its subdirectories, and its files:
'''


for (root, subs, files) in os.walk('.'):
    for name in files:
        if name.startswith('why'):
            print(root, name)

dw = os.walk('.')
print(type(dw))
print(dw is iter(dw))
