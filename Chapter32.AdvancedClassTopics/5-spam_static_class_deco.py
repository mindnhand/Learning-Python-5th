#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 5-spam_static_deco.py
# Description: Decoration rebinds the method name to the decorator's result.
#              The net effect is that calling the method function's name later 
#              actually triggers the result of its static method decorator first.
#              Because a decorator can return any sort of object, this allows the 
#              decorator to insert a layer of logic to be run on every call. The 
#              decorator function is free to return either the original function 
#              itself, or a new proxy object t    hat saves the original function 
#              passed to the decorator to be invoked indirectly after the extra 
#              logic layer runs.
#-----------------------------------------


# 所有从Spam类继承出来的子类都会共享Spam类的instance_counter这个计数器
class Spam:
    instance_counter = 0
    def __init__(self):
        Spam.instance_counter += 1
    @staticmethod
    def print_counter():
        print('Number of instances are created: %s' % Spam.instance_counter)

class SpamSub(Spam):
    instance_counter = 0
    def __init__(self):
        Spam.__init__(self)


# 让每个类各自保持自己的计数器
class Spam1:
    instance_counter = 0
    @classmethod
    def count(cls):
        cls.instance_counter += 1
    def __init__(self):
        self.count()
    @classmethod
    def print_counter(cls):
        print('Number of intances are created: %s' % cls.instance_counter)

class Spam1Sub(Spam1):
    instance_counter = 0 



if __name__ == '__main__':
    print('Spam class')
    a1 = Spam()
    a2 = Spam()
    a3 = Spam()
    Spam.print_counter()
    print()


    print('SpamSub class')
    as1 = SpamSub()
    as2 = SpamSub()
    as3 = SpamSub()
    SpamSub.print_counter()
    print()

    print('Spam1 class')
    b1 = Spam1()
    b2 = Spam1()
    b3 = Spam1()
    Spam1.print_counter()
    print()


    print('Spam1Sub class')
    b1 = Spam1Sub()
    b2 = Spam1Sub()
    b3 = Spam1Sub()
    Spam1Sub.print_counter()
    print()

    '''
    results: 
    Chapter32.AdvancedClassTopics]# python3 5-spam_static_class_deco.py 
    Spam class
    Number of instances are created: 3

    SpamSub class
    Number of instances are created: 6

    Spam1 class
    Number of intances are created: 3

    Spam1Sub class
    Number of intances are created: 3
    '''
