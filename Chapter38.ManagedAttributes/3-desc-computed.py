#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 3-desc-computed.py
# Description: computed attribute with attribute descriptor
#-----------------------------------------------


# Implementation 1
class DescSquare:
    def __init__(self, start):
        self.value = start
    def __get__(self, instance, owner):
        print('Descriptor DescSquare __get__ method...')
        return self.value ** 2
    def __set__(self, instance, value):
        print('Descriptor DescSquare __set__ method...')
        self.value = value
    def __delete__(self, instance):
        print('Descriptor DescSquare __delete__ method...')
        del self.value


class Client1:
    x = DescSquare(3)


class Client2:
    x = DescSquare(32)

# Implementation 2
class DescSquare1:
    def __get__(self, instance, owner):
        print('Descriptor DescSquare1 __get__ method...')
        return instance._value ** 2
    def __set__(self, instance, value):
        print('Descriptor DescSquare1 __set__ method...')
        instance._value = value
    def __delete__(self, instance):
        print('Descriptor DescSquare1 __delete__ method...')
        del instance._value

class Client3:
    def __init__(self, value):
        self._value = value
    x = DescSquare1()

class Client4:
    def __init__(self, value):
        self._value = value
    x = DescSquare1()


if __name__ == '__main__':
    c1 = Client1()
    c2 = Client2()
    print(c1.x)
    c1.x = 7
    print(c1.x)
    print(c2.x)
    print()

    print('-' * 20)
    c3 = Client3(9)
    c4 = Client4(45)
    print(c3.x)
    c3.x = 11
    print(c3.x)
    print(c4.x)
