#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage:
# Description:
#--------------------------------------------------



class Commuter1:
    def __init__(self, val):
        print('in Commuter1 instance')
        self.val = val
    def __add__(self, other):
        print('add', self.val, other)
        return self.val + other
    def __radd__(self, other):
        print('radd', self.val, other)
        return other + self.val

'''
For truly commutative operations that do not require special-casing by position, it is
also sometimes sufficient to reuse __add__ for __radd__: either by calling __add__ directly;
by swapping order and re-adding to trigger __add__ indirectly; or by simply assigning __radd__ 
to be an alias for __add__ at the top level of the class statement (i.e., in the class's scope). 
The following alternatives implement all three of these schemes, and return the same results as 
the original—though the last saves an extra call or dispatch and hence may be quicker (in all, 
__radd__ is run when self is on the right side of a +):
'''
class Commuter2:
    def __init__(self, val):
        print('in Commuter2 instance')
        self.val = val
    def __add__(self, other):
        print('add', self.val, other)
        return self.val + other
    def __radd__(self, other):
        return self.__add__(other)                  # Call __add__ explicitly


class Commuter3:
    def __init__(self, val):
        print('in Commuter3 instance')
        self.val = val
    def __add__(self, other):
        print('add', self.val, other)
        return self.val + other
    def __radd__(self, other):
        return self + other                         # Swap order and re-add


class Commuter4:
    def __init__(self, val):
        print('in Commuter4 instance')
        self.val = val
    def __add__(self, other):
        print('add', self.val, other)
        return self.val + other
    __radd__ = __add__                              # Alias: cut out the middleman
# 上述的的代码执行过程，可以通过http://www.pythontutor.com/live.html#mode=edit进行在线查看，可以
# 帮助更改好的理解上述的代码实现原理。
'''
In all these, right-side instance appearances trigger the single, shared __add__ method,
passing the right operand to self, to be treated the same as a left-side appearance. Run
these on your own for more insight; their returned values are the same as the original.
'''


'''
Propagating class type
In more realistic classes where the class type may need to be propagated in results,
things can become trickier: type testing may be required to tell whether it's safe to
convert and thus avoid nesting. For instance, without the isinstance test in the following,
we could wind up with a Commuter5 whose val is another Commuter5 when two instances are added 
and __add__ triggers __radd__:
'''
class Commuter5:                                    # Propagate class type in results
    def __init__(self, val):
        print('in Commuter5 instance')
        self.val = val
    def __add__(self, other):
        if isinstance(other, Commuter5):            # Type test to avoid object nesting
            other = other.val
        return Commuter5(self.val + other)          # Else + result is another Commuter
    def __radd__(self, other):
        return Commuter5(other + self.val)
    def __str__(self):
        return '<Commuter5: %s>' % self.val


if __name__ == '__main__':
    for klass in Commuter1, Commuter2, Commuter3, Commuter4:
        x = klass(88)
        y = klass(99)
        print('=' * 10 + 'call __add__ when x + 1')
        print(x + 1)                                    # __add__: instance + noninstance
        print()
        print('=' * 10 + 'call __radd__ when 1 + y')
        print(1 + y)                                    # __radd__: noninstance + instance
        print()
        print('=' * 10 + 'call __add__ and __radd__ when x + y')
        print(x + y)                                    # __add__: instance + instance, triggers __radd__
        print()
    else:
        print()

    print('=' * 20 + ' Test for Commuter5 class', end=' ')
    print('=' * 20)
    a = Commuter5(88)
    b = Commuter5(99)
    print('=' * 10 + 'call __add__ when x + 10')
    print(x + 10)                                   # Result is another Commuter instance
    print()
    print('=' * 10 + 'call __radd__ when 10 + y')
    print(10 + y)
    z = x + y                                       # Not nested: doesn't recur to __radd__
    print('=' * 10 + 'call __add__, __radd__ when x + y')
    print(z)

