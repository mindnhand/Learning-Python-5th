#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 lines_blocks_loop.py test.txt
# Description: read line by line from the file
#              or block by block 
#-------------------------------------------



import sys


i_f = sys.argv[1]


t_file = open(i_f)

print('In the while loop-1')
while True:
    line = t_file.readline()
    if not line:
        break
    print(line.rstrip())
print('End the while loop-1.')
print()


b_file = open(i_f, 'rb')

print('In the while loop-2')
while True:
    chunk = b_file.read(10)
    if not chunk:
        break
    print(chunk)
print('End the while loop-2.')
