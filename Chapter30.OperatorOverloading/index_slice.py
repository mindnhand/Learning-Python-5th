#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------
# Usage: python3 index_slice.py
# Description: slice and index
#------------------------------------------------------



'''
Our first method set allows your classes to mimic some of the behaviors of sequences
and mappings. If defined in a class (or inherited by it), the __getitem__ method is called
automatically for instance-indexing operations. When an instance X appears in an indexing
expression like X[i], Python calls the __getitem__ method inherited by the instance,
passing X to the first argument and the index in brackets to the second argument.

For example, the following class returns the square of an index value—atypical perhaps,
but illustrative of the mechanism in general:
'''


class Indexer:
    def __getitem__(self, index):
        return index ** 2


'''
Interestingly, in addition to indexing, __getitem__ is also called for slice expressions—
always in 3.X, and conditionally in 2.X if you don't provide more specific slicing methods.
'''
class Slicer:
    data = [5, 6, 7, 8, 9]
    def __getitem__(self, index):                   # Called for index or slice
        print('getitem: ', index)                   # the argument [m:n] is converted to slice(m, n, None), the place of None is step
        return self.data[index]


class SlicerTypeCheck:
    '''
    Where needed, __getitem__ can test the type of its argument, and extract slice object
    bounds—slice objects have attributes start, stop, and step, any of which can be None
    if omitted:
    '''
    def __getitem__(self, index):
        if isinstance(index, int):                  # Test usage mode
            print('indexing', index)
        else:
            print('slicing', index.start, index.stop, index.step)


class SliceSet:
    '''
    If used, the __setitem__ index assignment method similarly intercepts both index and
    slice assignments—in 3.X (and usually in 2.X) it receives a slice object for the latter,
    which may be passed along in another index assignment or used directly in the same
    way:
    '''
    def __init__(self, *seq):
        self.data = list(seq)
    def __setitem__(self, index, value):            # Intercept index or slice assignment
        i_start = index.start
        i_stop = index.stop
        i_step = index.step
        self.data[index] = value

'''
In fact, __getitem__ may be called automatically in even more contexts than indexing
and slicing -- it's also an iteration fallback option, as we'll see in a moment.
'''


'''
On a related note, don't confuse the (perhaps unfortunately named) __index__ method
in Python 3.X for index interception—this method returns an integer value for an instance
when needed and is used by built-ins that convert to digit strings
'''
class C:
    def __index__(self):
        return 2


'''
Here's a hook that isn't always obvious to beginners, but turns out to be surprisingly
useful. In the absence of more-specific iteration methods we’ll get to in the next section,
the for statement works by repeatedly indexing a sequence from zero to higher indexes,
until an out-of-bounds IndexError exception is detected. Because of that, __geti
tem__ also turns out to be one way to overload iteration in Python—if this method is
defined, for loops call the class's __getitem__ each time through, with successively
higher offsets.
'''
class StepperIndex:
    def __init__(self, *args):
        self.data = list(*args)
    def __getitem__(self, i):
        return self.data[i]



if __name__ == '__main__':
    print()
    print('=' * 20 + ' 1. ' + 'Test for Indexer')
    i = Indexer()
    a = i[2]                                        # x[i] calls x.__getitem__(i)
    print(a)
    print()


    for idx in range(5):
        print(i[idx], end=' ')                      # Runs __getitem__(x, i) each time
    else:
        print()
    print()


    print('=' * 20 + ' 2. ' + 'Test for Slicer')
    '''
    When called for slicing, though, the method receives a slice object, which is simply
    passed along to the embedded list indexer in a new index expression:

    When called for slicing, though, the method receives a slice object, which is simply
    passed along to the embedded list indexer in a new index expression:
    
    The index value [m, n, s] is converted to slice(m, n, s), for example:
    In [49]: l = [5, 6, 7, 8, 9]

    In [50]: l[slice(None, None, 2)]
    Out[50]: [5, 7, 9]

    In [51]: l[::2]
    Out[51]: [5, 7, 9]
    '''
    s = Slicer()
    a0 = s[0]
    a1to3 = s[1:4]                                  # Slicing sends __getitem__ a slice object
    print(a1to3)
    a1toend = s[1:]
    print(a1toend)
    a0to_1 = s[:-1]
    print(a0to_1)
    a0toend_step2 = s[::2]
    print(a0toend_step2)
    print()

    print('=' * 20 + ' 3. ' + 'Test for SlicerTypeCheck')
    stc = SlicerTypeCheck()
    stc[99]
    stc[1:99:2]
    stc[1:]
    print()

    print('=' * 20 + ' 4. ' + 'Test for SliceSet')
    ss = SliceSet(1, 2, 3, 4, 5)
    print(ss.data)
    ss[1:3] = (7, 8)
    print(ss.data)
    print()

    print('Test for C')
    c = C()
    l = [1, 2, 3, 4, 5]
    print(c)
    '''
    Although this method does not intercept instance indexing like __getitem__, it is also
    used in contexts that require an integer—including indexing:
    '''
    print(l[c])                                     # As index, not c[i:]
    print()


    print('=' * 20 + ' 5. ' + 'Test for SliceSet')
    si = StepperIndex('spam')
    print(si[1])
    for x in si:
        print(x, end=' ')
    else:
        print()
    print('p' in si)
    print([x for x in si])
    print(list(map(str.upper, si)))
    print(list(si), tuple(si), ' '.join(si), sep=' <=> ')
