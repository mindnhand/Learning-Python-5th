#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 4-getattr-computed.py
# Description: operator overloading
#------------------------------------------------



class AttrSquare:
    def __init__(self, start):
        self.value = start 			# Triggers __setattr__!
    def __getattr__(self, attr): 		# On undefined attr fetch
        if attr == 'X':
            return self.value ** 2 	# value is not undefined
        else:
            raise AttributeError(attr)
    def __setattr__(self, attr, value): 	# On all attr assignments
        if attr == 'X':
            attr = 'value'
        #self.__dict__[attr] = value            # method 1 
        object.__setattr__(self, attr, value)   # method 2



if __name__ == '__main__':
    A = AttrSquare(3) 			# 2 instances of class with overloading
    B = AttrSquare(32) 			# Each has different state information
    print(A.X) 			# 3 ** 2
    A.X = 4
    print(A.X)            # 4 ** 2
    print(B.X)            # 32 ** 2 (1024)
