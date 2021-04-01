#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 4-descriptor_to_compute_attribute.py
# Description: attribute management 2 of 4
#              Same, but with descriptors (per-instance state)
#--------------------------------------------


class DescSquare(object):
    def __get__(self, instance, owner):
        return instance._square ** 2
    def __set__(self, instance, value):
        instance._square = value

class DescCube(object):
    def __get__(self, instance, owner):
        return instance._cube ** 3
    def __set__(self, instance, value):
        instance._cube = value

class Powers(object): 			# Need all (object) in 2.X only
    square = DescSquare()
    cube = DescCube()
    def __init__(self, square, cube):
        self._square = square 	        # "self.square = square" works too,
        self._cube = cube 		# because it triggers desc __set__!



if __name__ == '__main__':
    X = Powers(3, 4)
    print(X.square) 		# 3 ** 2 = 9
    print(X.cube) 		# 4 ** 3 = 64
    X.square = 5
    print(X.square) 		# 5 ** 2 = 25

    X.cube = 7
    print(X.cube)
