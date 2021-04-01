#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------
# Usage: python3 4-delegation.py
# Description: delegation pattern
#--------------------------------------



'''
Because all attributes are routed to our interception methods generically, 
we can validate and pass them along to embedded, managed objects.
'''

class Wrapper:
    def __init__(self, object):
        self.wrapped = object 				# Save object
    def __getattr__(self, attrname):
        print('Trace: ' + attrname) 			# Trace fetch
        return getattr(self.wrapped, attrname) 	# Delegate fetch



if __name__ == '__main__':
    X = Wrapper([1, 2, 3])
    X.append(4) 				# Prints "Trace: append"
    print(X.wrapped) 			# Prints "[1, 2, 3, 4]"
