#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 proxy_coding.py
# Description: proxy coding requirements
#-------------------------------------------


'''
The net effect: to code a proxy of an object whose interface
may in part be invoked by built-in operations, new-style classes
require both __getattr__ for normal names, as well as method 
redefinitions for all names accessed by built-in operations -- whether
coded manually, obtained from superclasses, or generated by tools.
When redefinitions are so incorporated, calls through both instances
and types are equivalent to built-in operations, though redefined
names are no longer routed to the generic __getattr__ undefined name
handler, even for explicit name calls:
'''


class C(object):                            # new-style class
    data = 'spam'
    def __getattr__(self, name):            # catch normal name
        print('getattr: ' + name)
        return getattr(self.data, name)

    def __getitem__(self, idx):             # redefine builtins
        print('getitem: ' + str(idx))
        return self.data[idx]               # run expr or getattr
    
    def __add__(self, other):
        print('add: ' + other)
        return getattr(self.data, '__add__')(other)



if __name__ == '__main__':
    x = C()
    print(x.upper())
    print(x[1])
    print(x + 'eggs')
    print(type(x).__add__(x, 'eggs'))