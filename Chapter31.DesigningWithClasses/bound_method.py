#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 bound_method.py
# Description: bound methods
#----------------------------------------------



class Number:
    def __init__(self, base):
        self.base = base
    def double(self):
        return self.base * 2
    def triple(self):
        return self.base * 3




if __name__ == '__main__':
    x = Number(2) 		# Class instance objects
    y = Number(3) 		# State + methods
    z = Number(4)

    xv = x.double() 			# Normal immediate calls
    print(xv)
    
    acts = [x.double, y.double, y.triple, z.double]      # List of bound methods
    for act in acts: 		# Calls are deferred
        print(act()) 				# Call as though functions
