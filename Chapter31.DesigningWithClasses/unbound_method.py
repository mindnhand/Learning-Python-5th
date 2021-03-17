#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 selfless.py
# Description: unbound method in python3.x is called simple function
#-----------------------------------------------



class Selfless:
    def __init__(self, data):
        self.data = data
    def selfless(arg1, arg2): 		# A simple function in 3.X
        return arg1 + arg2
    def normal(self, arg1, arg2): 	# Instance expected when called
        return self.data + arg1 + arg2



if __name__ == '__main__':
    X = Selfless(2)
    print(X.normal(3, 4)) 						# Instance passed to self automatically: 2+(3+4)
    print(Selfless.normal(X, 3, 4)) 				# self expected by method: pass manually
    print(Selfless.selfless(3, 4)) 				# No instance: works in 3.X, fails in 2.X!
