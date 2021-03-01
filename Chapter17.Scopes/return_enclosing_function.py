#!/usr/bin/env python3
#encoding=utf-8



#--------------------------------------------
# Usage: python3 return_enclosing_function.py
# Description: enclosing function, the basic 
#              pattern of factory function
#--------------------------------------------



def f1():
    x = 88
    def f2():
        print(x)        # Remembers x in enclosing def scope
    return f2           # Return f2 but don't call it


action = f1()           # Make, return f2 function

action()                # Call it now: prints 88
