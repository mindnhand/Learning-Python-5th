#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 4-operator-overloading_to_compute_attribute.py
# Description: attribute management 3 of 4
#              Same, but with generic __getattr__ undefined attribute interception
#-----------------------------------------



class Powers:
    def __init__(self, square, cube):
        self._square = square
        self._cube = cube
    def __getattr__(self, name):
        if name == 'square':
            return self._square ** 2
        elif name == 'cube':
            return self._cube ** 3
        else:
            raise TypeError('unknown attr:' + name)
    def __setattr__(self, name, value):
        if name == 'square':
            self.__dict__['_square'] = value 			# Or use object
        elif name == 'cube':
            self.__dict__['_cube'] = value
        else:
            self.__dict__[name] = value



if __name__ == '__main__':
    X = Powers(3, 4)
    print(X.square) 			# 3 ** 2 = 9
    print(X.cube) 			# 4 ** 3 = 64
    X.square = 5
    print(X.square) 			# 5 ** 2 = 25

    X.cube = 7
    print(X.cube)
