#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 squares.py
# Description: iterable object with __iter__ method
#-----------------------------------------------


class Squares:
    def __init__(self, start, stop):                    # Save state when created
        self.value = start - 1
        self.stop = stop
    def __iter__(self):                                 # Get iterator object on iter
        return self
    def __next__(self):                                 # Return a square on each iteration
        print('calling __next__')
        if self.value == self.stop:                     # Also called by next builtin
            raise StopIteration
        self.value += 1
        return self.value ** 2

'''
Here, the iterator object returned by __iter__ is simply the instance self, because the
__next__ method is part of this class itself. In more complex scenarios, the iterator
object may be defined as a separate class and object with its own state information to
support multiple active iterations over the same data (we’ll see an example of this in a
moment). The end of the iteration is signaled with a Python raise statement—introduced
in Chapter 29 and covered in full in the next part of this book, but which simply
raises an exception as if Python itself had done so.
'''


if __name__ == '__main__':
    sq = Squares(1, 5)
    for i in sq:                                        # for calls iter, which calls __iter__
        print(i, end=' ')                               # Each iteration calls __next__
    else:
        print()

    '''
    An equivalent coding of this iterable with __getitem__ might be less natural, because
    the for would then iterate through all offsets zero and higher; the offsets passed in
    would be only indirectly related to the range of values produced (0..N would need to
    map to start..stop). Because __iter__ objects retain explicitly managed state between
    next calls, they can be more general than __getitem__.
    On the other hand, iterables based on __iter__ can sometimes be more complex and
    less functional than those based on __getitem__. They are really designed for iteration,
    not random indexing—in fact, they donn't overload the indexing expression at all,
    though you can collect their items in a sequence such as a list to enable other operations:
    '''
    #print(sq[1])                                        # This will raise Exception

    '''
    Single versus multiple scans
    The __iter__ scheme is also the implementation for all the other iteration contexts we
    saw in action for the __getitem__ method—membership tests, type constructors, sequence
    assignment, and so on. Unlike our prior __getitem__ example, though, we also
    need to be aware that a class's __iter__ may be designed for a single traversal only, not
    many. Classes choose scan behavior explicitly in their code.

    For example, because the current Squares class's __iter__ always returns self with just
    one copy of iteration state, it is a one-shot iteration; once you've iterated over an instance
    of that class, it's empty. Calling __iter__ again on the same instance returns
    self again, in whatever state it may have been left. You generally need to make a new
    iterable instance object for each new iteration:
    '''
    print([x for x in sq])                              # This will output an empty list
    sq = Squares(1, 5)                                  # Make a new iterable object
    print([x for x in sq])

    '''
    Just like single-scan built-ins such as map, converting to a list supports multiple scans
    as well, but adds time and space performance costs, which may or may not be significant
    to a given program:
    '''
    x = list(Squares(1, 5))
    print(tuple(x), tuple(x))

    '''
    Moreover, we're not required to make a new string or convert to a list each time; 
    the single string object itself supports multiple scans.
    We saw related examples earlier, in Chapter 14 and Chapter 20. For instance, generator
    functions and expressions, as well as built-ins like map and zip, proved to be singleiterator
    objects, thus supporting a single active scan. By contrast, the range built-in,
    and other built-in types like lists, support multiple active iterators with independent
    positions.
    '''

