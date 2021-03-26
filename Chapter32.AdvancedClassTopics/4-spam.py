#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------
# Usage: python3 4-spam.py
# Description: class has a counter stored as a class attribute, a constructor 
#              that bumps up the counter by one each time a new instance is 
#              created, and a method that displays the counter's value.
#----------------------------------


class Spam:
    instance_counter = 0
    def __init__(self):
        Spam.instance_counter += 1

    def print_counter():
        print('Number of instances created: %s' % Spam.instance_counter)


# mutation of Spam
'''
Short of marking a self-less method as special, you can sometimes achieve 
similar results with different coding structures. For example, if you just
want to call functions that access class members without an instance, perhaps 
the simplest idea is to use normal functions outside the class, not class 
methods. This way, an instance isn't expected in the call. The following 
mutation of spam.py illustrates, and works the same in Python 3.X and 2.X:
'''
class SpamMuta:
    instance_counter = 0
    def __init__(self):
        SpamMuta.instance_counter += 1


def print_instance_counter():
    print('Number of instances created: %s' % SpamMuta.instance_counter)


if __name__ == '__main__':
    a = Spam()
    b = Spam()
    c = Spam()
    Spam.print_counter()

    print()
    print('Following is SpamMuta class')
    a1 = SpamMuta()
    a2 = SpamMuta()
    a3 = SpamMuta()
    print_instance_counter()
    print()
