#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 5-registry-deco.py
# Descripiton: Registering decorated objects to an API
#-----------------------------------------------



registry = {}


def register(obj):             # both class and function decorator
    registry[obj.__name__] = obj        # registry object, add an object to the registry dict
    return obj                  # return obj itself, not a wrapper

@register
def spam(x):
    return x ** 2


@register
def ham(x):
    return x ** 3


@register
class Eggs:
    def __init__(self, x):
        self.data = x ** 4
    def __str__(self):
        return str(self.data)


if __name__ == '__main__':
    print('Registry: ')
    for name in registry:
        print(name, '==>', registry[name], type(registry[name]))

    print('\nManual call: ')
    print(spam(2))
    print(ham(2))
    x = Eggs(2)
    print(x)

    print('\nRegistry calls: ')
    for name in registry:
        print(name, '==>', registry[name](2))
