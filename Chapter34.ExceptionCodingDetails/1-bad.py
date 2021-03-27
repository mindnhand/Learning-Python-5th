#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 1-bad.py
# Description: Because the program ignores the exception it triggers, 
#              Python kills the program and prints a message
#-------------------------------------------


def gobad(x, y):
    return x / y

def gosouth(x):
    print(gobad(x, 0))


gosouth(1)


'''
results:
    Chapter34.ExceptionCodingDetails]# python3 1-bad.py
    Traceback (most recent call last):
      File "1-bad.py", line 19, in <module>
        gosouth(1)
      File "1-bad.py", line 16, in gosouth
        print(gobad(x, 0))
      File "1-bad.py", line 13, in gobad
        return x / y
    ZeroDivisionError: division by zero
'''
