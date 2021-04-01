#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------
# Usage: python3 4-getattr-v-getattribute.py
# Description: compare the __getattr__ and __getattribute__
#----------------------------------



'''
To summarize the coding differences between __getattr__ and __getattribute__, 
the following example uses both to implement three attributes -- attr1 is a 
class attribute, attr2 is an instance attribute, and attr3 is a virtual managed 
attribute computed when fetched
'''




class GetAttr:
    attr1 = 1
    def __init__(self):
        self.attr2 = 2
    def __getattr__(self, attr):        # On undefined attrs only
        print('get: ' + attr)           # Not on attr1: inherited from class
        if attr == 'attr3':             # Not on attr2: stored on instance
            return 3
        else:
            raise AttributeError(attr)


class GetAttribute(object):             # (object) needed in 2.X only
    attr1 = 1
    def __init__(self):
        self.attr2 = 2
    def __getattribute__(self, attr):   # On all attr fetches
        print('get: ' + attr)           # Use superclass to avoid looping here
        if attr == 'attr3':
            return 3
        else:
            return object.__getattribute__(self, attr)




if __name__ == '__main__':
    # test for __getattr__
    print('The result of __getattr__')
    X = GetAttr()
    print(X.attr1)
    print(X.attr2)
    print(X.attr3)
    print()
    print('-'*20)
    
    
    # test for __getattribute__
    print('The result of __getattribute__')
    X = GetAttribute()
    print(X.attr1)
    print(X.attr2)
    print(X.attr3)
    print(X.attr4)
