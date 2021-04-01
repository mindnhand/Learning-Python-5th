#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------
# Usage: python3 4-getattribute-computed.py
# Description: 
#----------------------------------------


'''
we can achieve the same effect with __getattribute__ instead of __getattr__; the following
replaces the fetch method with a __getattribute__ and changes the __setattr__ assignment
method to avoid looping by using direct superclass method calls instead of __dict__ keys
'''

class AttrSquare: 				# Add (object) for 2.X
    def __init__(self, start):
        print('in __init__ method')
        self.value = start 		# Triggers __setattr__!
    def __getattribute__(self, attr): 		# On all attr fetches
        print('in __getattribute__ method')
        if attr == 'X':
            # the result1 in the end of the file
            #return self.value ** 2 			# Triggers __getattribute__ again!

            # the result2 in the end of the file
            return object.__getattribute__(self, 'value') ** 2      # avoid triggers __getattribute__ again!
        else:
            return object.__getattribute__(self, attr)
    def __setattr__(self, attr, value): 		# On all attr assignments
        print('in __setattr__ method')
        if attr == 'X':
            attr = 'value'
        object.__setattr__(self, attr, value)           # method 1
        #self.__dict__[attr] = value                     # method 2




if __name__ == '__main__':
    print('1. initialize instance A and B')
    A = AttrSquare(3) 			# 2 instances of class with overloading
    B = AttrSquare(32) 			# Each has different state information
    
    print('\n2. fetch attribute of A')
    print(A.X) 			# 3 ** 2

    print('\n3. assing attribute of A')
    A.X = 4

    print('\n4. fetch attribute of A')
    print(A.X)            # 4 ** 2

    print('\n5. fetch attribute of B')
    print(B.X)            # 32 ** 2 (1024)


    # the result1 in the end of the file
    '''
    Chapter38.ManagedAttributes]# python3 4-getattribute-computed.py                                                                  
    1. initialize instance A and B
    in __init__ method
    in __setattr__ method
    in __init__ method
    in __setattr__ method

    2. fetch attribute of A
    in __getattribute__ method
    in __getattribute__ method
    9

    3. assing attribute of A
    in __setattr__ method

    4. fetch attribute of A
    in __getattribute__ method
    in __getattribute__ method
    16

    5. fetch attribute of B
    in __getattribute__ method
    in __getattribute__ method
    1024
    '''


    # the result2 in the end of the file
    '''
    Chapter38.ManagedAttributes]# python3 4-getattribute-computed.py
    1. initialize instance A and B
    in __init__ method
    in __setattr__ method
    in __init__ method
    in __setattr__ method

    2. fetch attribute of A
    in __getattribute__ method
    9

    3. assing attribute of A
    in __setattr__ method

    4. fetch attribute of A
    in __getattribute__ method
    16

    5. fetch attribute of B
    in __getattribute__ method
    1024
    '''
