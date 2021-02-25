#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------
# Usage: python3 continue.py
# Description: example for continue
#--------------------------------


x = 10

print('even result: ', end='')
while x:
    x -= 1      # x = x - 1
    if x % 2 != 0:
        continue
    print(x, end=' ')
else:
    print()



# similar implementation with the followed code 
y = 10

print('even result: ', end='')
while y:
    y -= 1
    if y % 2 == 0:
        print(y, end=' ')
else:
    print()
