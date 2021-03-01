#!/usr/bin/env python3
#encoding=utf-8



#--------------------------------------------------
# Usage: ipython
#        In [1]: import os
#        In [2]: os.chdir('/path/to/makeopen.py/')
#        In [3]: from makeopen import makeopen
#        In [4]: F = open('script2.py')
#        In [5]: F.read()
#        Out[5]: 'import sys\nprint(sys.path)\nx = 2\nprint(x ** 32)\n'
#        In [6]: makeopen('spam')
#        In [7]: G = open('script2.py')
#        Custom open call 'spam':  ('script2.py',) {}
#        In [8]: G.read()
#        Out[8]: 'import sys\nprint(sys.path)\nx = 2\nprint(x ** 32)\n'
#        In [9]: makeopen('eggs')
#        In [10]: L = open('script2.py')
#        Custom open call 'eggs':  ('script2.py',) {}
#        Custom open call 'spam':  ('script2.py',) {}
#        In [11]: L.read()
#        Out[11]: 'import sys\nprint(sys.path)\nx = 2\nprint(x ** 32)\n'
#        In [12]: builtins.open = io.open
#        ---------------------------------------------------------------------------
#        NameError                                 Traceback (most recent call last)
#        <ipython-input-12-ba8063ce1bc2> in <module>
#        ----> 1 builtins.open = io.open
#        NameError: name 'io' is not defined
#        In [13]: import io
#        In [14]: builtins.open = io.open---------------------------------------------------------------------------
#        NameError                                 Traceback (most recent call last)
#        <ipython-input-14-ba8063ce1bc2> in <module>
#        ----> 1 builtins.open = io.open
#        NameError: name 'builtins' is not defined
#        In [15]: open
#        Out[15]: <function makeopen.makeopen.<locals>.custom(*args, **kwargs)>
#        In [16]: open = io.open
#        In [17]: open
#        Out[17]: <function io.open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)>
#--------------------------------------------------



import builtins


def makeopen(id):
    original = builtins.open
    def custom(*args, **kwargs):
        print('Custom open call %r: ' % id, args, kwargs)
        return original(*args, **kwargs)
    builtins.open = custom


class MakeOpenClass:
    def __init__(self, id):
        self.id = id
        self.original = builtins.open
        builtins.open = self
    def __call__(self, *args, **kwargs):
        print('Custom open call %r: ' % self.id, args, kwargs)
        return self.original(*args, **kwargs)
