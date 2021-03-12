#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 docstr.py
# Description: doc string
#-----------------------------------------



"I am: docstr.__doc__"


def func(args):
    'I am: docstr.func.__doc__'
    pass


class spam:
    'I am: spam.__doc__ or docstr.spam.__doc__ or self.__doc__'
    def method(self):
        'I am: spam.method.__doc__ or self.method.__doc__'
        print(self.__doc__)
        print(self.method.__doc__)

'''
The main advantage of documentation strings is that they stick around at runtime.
Thus, if it’s been coded as a docstring, you can qualify an object with its __doc__ attribute
to fetch its documentation (printing the result interprets line breaks if it's a
multiline string):
>>> import docstr
>>> docstr.__doc__
'I am: docstr.__doc__'
>>> docstr.func.__doc__'I am: docstr.func.__doc__'
>>> docstr.spam.__doc__
'I am: spam.__doc__ or docstr.spam.__doc__ or self.__doc__'
>>> docstr.spam.method.__doc__'I am: spam.method.__doc__ or self.method.__doc__'
>>> x = docstr.spam()
>>> x.method()
I am: spam.__doc__ or docstr.spam.__doc__ or self.__doc__
I am: spam.method.__doc__ or self.method.__doc__
>>> help(docstr)
Help on module docstr:
    NAME
    docstr - I am: docstr.__doc__FILE
    c:\code\docstr.py
    CLASSES
    spam
    class spam
    | I am: spam.__doc__ or docstr.spam.__doc__ or self.__doc__
    |
    | Methods defined here:
        |
        | method(self)
        | I am: spam.method.__doc__ or self.method.__doc__
        FUNCTIONS
        func(args)
        I am: docstr.func.__doc__

Documentation strings are available at runtime, but they are less flexible syntactically
than # comments, which can appear anywhere in a program. Both forms are useful
tools, and any program documentation is good (as long as it's accurate, of course!). As
stated before, the Python "best practice" rule of thumb is to use docstrings for functional
documentation (what your objects do) and hash-mark comments for more microlevel 
documentation (how arcane bits of code work).
'''

