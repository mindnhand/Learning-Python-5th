#!/usr/bin/env python3 
#encoding=utf-8


#----------------------------------------------
# Usage: python squares_yield.py
# Description: For example, the following class is equivalent to the initial Squares user-defined iterable
#              we coded earlier in squares.py.
#----------------------------------------------



class Squares:                                  # __iter__ + yield generator
    def __init__(self, start, stop):            # __next__ is automatic/implied
        self.start = start
        self.stop = stop
    def __iter__(self):
        for value in range(self.start, self.stop + 1):
            yield value ** 2
    '''
    It may also help to notice that we could name the generator method something other
    than __iter__ and call manually to iterate—Squares(1,5).gen(), for example. Using
    the __iter__ name invoked automatically by iteration tools simply skips a manual attribute
    fetch and call step:
    '''
    def gen(self):
        for value in range(self.start, self.stop + 1):
            yield value ** 2



if __name__ == '__main__':
    for i in Squares(1, 5):
        print(i, end=' ')
    else:
        print()

    '''
    And as usual, we can look under the hood to see how this actually works in iteration
    contexts. Running our class instance through iter obtains the result of calling
    __iter__ as usual, but in this case the result is a generator object with an automatically
    created __next__ of the same sort we always get when calling a generator function that
    contains a yield. The only difference here is that the generator function is automatically
    called on iter. Invoking the result object’s next interface produces results on demand:
    '''
    S = Squares(1, 5)                           # Runs __init__: class saves instance state
    I = iter(S)                                 # Runs __iter__: returns a generator
    print(next(I))                              # Runs generator's __next__
    print(next(I))
    print()

    for i in Squares(1, 5).gen():
        print(i, end=' ')

    S1 = Squares(1, 5)
    I1 = iter(S1.gen())                         # Call generator manually for iterable/iterator
    next(I)
    '''
    Coding the generator as __iter__ instead cuts out the middleman in your code, though
    both schemes ultimately wind up creating a new generator object for each iteration:
    - With __iter__, iteration triggers __iter__, which returns a new generator with
      __next__.
    - Without __iter__, your code calls to make a generator, which returns itself for
      __iter__.

    See Chapter 20 for more on yield and generators if this is puzzling, and compare it
    with the more explicit __next__ version in squares.py earlier. You'll notice that this new
    squares_yield.py version is 4 lines shorter (7 versus 11). In a sense, this scheme reduces
    class coding requirements much like the closure functions of Chapter 17, but in this
    case does so with a combination of functional and OOP techniques, instead of an alternative
    to classes. For example, the generator method still leverages self attributes.
    This may also very well seem like one too many levels of magic to some observers—it
    relies on both the iteration protocol and the object creation of generators, both of which
    are highly implicit (in contradiction of longstanding Python themes: see import this).
    Opinions aside, it's important to understand the non-yield flavor of class iterables too,
    because it's explicit, general, and sometimes broader in scope.
    Still, the __iter__/yield technique may prove effective in cases where it applies. It also
    comes with a substantial advantage—as the next section explains.
    '''

    print('Test for multiple iteration')
    S2 = Squares(1, 3)
    for i in S2:                                # Each for calls __iter__
        for j in S2:
            print('%s:%s' % (i, j), end=' ')
    else:
        print()
    '''
    Besides its code conciseness, the user-defined class iterable of the prior section based
    upon the __iter__/yield combination has an important added bonus—it also supports
    multiple active iterators automatically. This naturally follows from the fact that each
    call to __iter__ is a call to a generator function, which returns a new generator with its
    own copy of the local scope for state retention.

    Although generator functions are single-scan iterables, the implicit calls to __iter__ in
    iteration contexts make new generators supporting new independent scans:
    '''
