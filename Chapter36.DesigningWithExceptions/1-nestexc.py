#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 1-nestexc.py
# Description: defines two functions. action2 is coded to trigger an exception
#              (you can't add numbers and sequences), and action1 wraps a call
#              to action2 in a try handler, to catch the exception
#----------------------------------------------



def action2():
    print(1 + [])               # Generate TyepError

def action1():
    try:
        action2()
    except TypeError:           # Most recent matching try
        print('inner try')


try:
    action1()
except TypeError:               # Here, only if action1 re-raise
    print('outer try')


# integrate action1 and outer-try
def action3():
    try:
        try:
            action2()
        except TypeError:
            print('inner try')
    except TypeError:
        print('outer try')


action3()
