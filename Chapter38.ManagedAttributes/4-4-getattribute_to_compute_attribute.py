#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 4-getattribute_to_compute_attribute.py
# Description: attribute management 4 of 4
#              Same, but with generic __getattribute__ all attribute interception
#-------------------------------------------------



class Powers(object): 			# Need (object) in 2.X only
    def __init__(self, square, cube):
        self._square = square
        self._cube = cube
    def __getattribute__(self, name):
        if name == 'square':
            return object.__getattribute__(self, '_square') ** 2         # call superclass's __getattribute__, avoid recursive loop
        elif name == 'cube':
            return object.__getattribute__(self, '_cube') ** 3       # call superclass's __getattribute__, avoid recursive loop
        else:
            return object.__getattribute__(self, name)       # call superclass's __getattribute__, avoid recursive loop
    def __setattr__(self, name, value):
        if name == 'square':
            object.__setattr__(self, '_square', value) # Or use __dict__
        elif name == 'cube':
            object.__setattr__(self, '_cube', value)
        else:
            object.__setattr__(self, name , value)
 



if __name__ == '__main__':
    X = Powers(3, 4)
    print(X.square) 			# 3 ** 2 = 9
    print(X.cube) 			# 4 ** 3 = 64
    X.square = 5
    print(X.square) 			# 5 ** 2 = 25

    X.cube = 7
    print(X.cube)
