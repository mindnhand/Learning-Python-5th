#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 
# Description: descriptior state information and 
#              client class's instance state information
#--------------------------------------------


'''
Both descriptor and instance state have roles. In fact, this 
is a general advantage that descriptors have over properties
-- because they have state of their own, they can easily retain
data internally, without adding it to the namespace of the
client instance object.

DescBoth's self.data retains per-attribute information, while 
Client's instance.data can vary per client instance
'''


class DescBoth:
    def __init__(self, data):
        self.data = data
    def __get__(self, instance, owner):
        return '%s, %s' % (self.data, instance.data)
    def __set__(self, instance, value):
        instance.data = value



class Client:
    def __init__(self, data):
        self.data = data
    managed = DescBoth('spam')




if __name__ == '__main__':
    I = Client('eggs')
    print(I.managed)

    I.managed = 'SPAM'
    print(I.managed)

    '''
    results:
    Chapter38.ManagedAttributes]# python3 3-desc-both-state.py
    spam, eggs
    spam, SPAM
    '''
