#!/usr/bin/env python3 
#encoding=utf-8


#--------------------------------------------
# Usage: python3 skipper.py
# Description: Implement multiple scan iterable object like a list with __iter__ and __next__
#--------------------------------------------



'''
When we code user-defined iterables with classes, it's up to us to decide whether we
will support a single active iteration or many. To achieve the multiple-iterator effect,
__iter__ simply needs to define a new stateful object for the iterator, instead of returning
self for each iterator request.
The following SkipObject class, for example, defines an iterable object that skips every
other item on iterations. Because its iterator object is created anew from a supplemental
class for each iteration, it supports multiple active loops directly (this is file skipper.
py in the book's examples):
'''


class SkipObject:
    def __init__(self, wrapped):                        # Save item to be used
        self.wrapped = wrapped
    def __iter__(self):
        return SkipIterator(self.wrapped)               # New iterator each time



class SkipIterator:
    def __init__(self, wrapped):
        self.wrapped = wrapped                          # Iterator state information
        self.offset = 0
    def __next__(self):
        if self.offset >= len(self.wrapped):            # Termination iterations
            raise StopIteration
        else:
            item = self.wrapped[self.offset]            # else return and skip
            self.offset += 2
            return item





if __name__ == '__main__':
    alpha = 'abcdef'
    skipper = SkipObject(alpha)                         # Make container object
    I = iter(skipper)                                   # Make an iterator on it
    print(next(I), next(I), next(I))                    # Visit offsets 0, 2, 4

    for x in skipper:                                   # for calls __iter__ automatically
        for y in skipper:                               # Nested fors call __iter__ again each time
            print(x + y, end=' ')                       # Each iterator has its own state, offset
    else:
        print()

    '''
    Here, there is just one SkipOb ject iterable, with multiple iterator objects created from it.
    '''
