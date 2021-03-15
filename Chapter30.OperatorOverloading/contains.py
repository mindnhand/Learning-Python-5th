#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 contains.py
# Description: membership, __contains__ -> __iter__ -> __getitem__ 
#---------------------------------------------

'''
As is, the class in this file has an __iter__ that supports multiple scans, but only a single
scan can be active at any point in time (e.g., nested loops won't work), because each
iteration attempt resets the scan cursor to the front.
'''

class Iters:
    def __init__(self, value):
        self.data = value
    def __getitem__(self, i):                           # Fallback for iteration
        print('get[%s]: ' % i, end='')                  # Also for index, slice
        return self.data[i]
    def __iter__(self):                                 # Prefered for iteration
        print('iter=> ', end='')                        # Allows only one active iterator
        self.ix = 0
        return self
    def __next__(self):
        print('next:', end='')
        if self.ix == len(self.data):
            raise StopIteration
        item = self.data[self.ix]
        self.ix += 1
        return item
    def __contains__(self, x):                          # Preferred for 'in'
        print('contains: ', end='')
        return x in self.data



if __name__ == '__main__':
    X = Iters([1, 2, 3, 4, 5])                          # Make instance
    print(3 in X)                                       # Membership
    for i in X:                                         # for loop
        print(i, end=' | ')
    else:
        print()
        
    print([i ** 2 for i in X])                          # Other iteration contexts
    print(list(map(bin, X)))

    I = iter(X)                                         # Manual iteration (what other contexts do)
    while True:
        try:
            print(next(I), end=' @ ')
        except StopIteration:
            break
    print()
    print(X[1])
