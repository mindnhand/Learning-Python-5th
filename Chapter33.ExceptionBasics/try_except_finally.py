#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 try_except_finally.py
# Description: 
#-------------------------------------------


def fetcher(obj, idx):
    return obj[idx]


# 1. without except, the last print('after try') will never be executed
#try:
#    s = 'spam'
#    val = fetcher(s, 4)
#finally:
#    print('after fetch')
#
#print('after try')

'''
results:
Chapter33.ExceptionBasics]# python3 try_except_finally.py 
after fetch
Traceback (most recent call last):
File "try_except_finally.py", line 18, in <module>
val = fetcher(s, 4)
File "try_except_finally.py", line 12, in fetcher
return obj[idx]
IndexError: string index out of range
'''

# 2. with except, after finally print, will execute the last print
try:
    s = 'spam'
    val = fetcher(s, 4)
except:
    print('in except')
finally:
    print('after fetch')

print('after try')

'''
results:
    Chapter33.ExceptionBasics]# python3 try_except_finally.py
    in except
    after fetch
    after try
'''
