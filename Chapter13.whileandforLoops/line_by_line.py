#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------
# Usage: python3 line_by_line.py test.txt
# Description: read by lines
#----------------------------------------


import sys


i_f = sys.argv[1]
t_file_lines = open(i_f).readlines()

for line in t_file_lines:
    print(line.rstrip())



print()
t_file = open(i_f)
# This is the best method to read a file
'''
The last example is also generally the best option for text files—besides its simplicity,
it works for arbitrarily large files because it doesn’t load the entire file into memory all
at once. The iterator version may also be the quickest, though I/O performance may
vary per Python line and release.
'''
for line in t_file:
    print(line.rstrip())
