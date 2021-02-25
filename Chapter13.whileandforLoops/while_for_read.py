#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 while_for_read.py test.txt
# Description: read the whole file into the memory
#------------------------------------------


import sys


i_f = sys.argv[1]

file = open(i_f)

print('In while loop:')
while True:
    char = file.read()
    if not char:
        break
    print(char, end='')
print('End the while loop.')
print()



print('In the for loop')
for char in open(i_f).read():
    print(char, end='')
else:
    print('End the for loop.')
