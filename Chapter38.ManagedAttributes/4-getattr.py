#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 4-getattr.py
# Description: get and set attribute with operator overloading
#---------------------------------------------



class Catcher:
    def __getattr__(self, name):
        print('Get: %s' % name)
    def __setattr__(self, name, value):
        print('Set: %s %s' % (name, value))

class Catcher1:
    def __getattribute__(self, name):
        print('Get: %s' % name)
    def __setattr__(self, name, value):
        print('Set: %s %s' % (name, value))

if __name__ == '__main__':
    X = Catcher()
    X.job 			# Prints "Get: job"
    X.pay 			# Prints "Get: pay"
    X.pay = 99 		# Prints "Set: pay 99"
    print()

    print('-' * 40)
    X1 = Catcher1()
    X1.job
    X1.pay
    X1.pay = 100

