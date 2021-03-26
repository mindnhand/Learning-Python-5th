#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------
# Usage: python3 5-tracer2.py
# Description: by using nested functions with enclosing scopes for state, instead of 
#              callable class instances with attributes, function decorators often 
#              become more broadly applicable to class-level methods too. We'll postpone 
#              the full details on this, but here's a brief look at this closure based
#              coding model; it uses function attributes for counter state for portability, 
#              but could leverage variables and nonlocal instead in 3.X only
#-----------------------------------



def tracer(func):                           # Remeber original
    def oncall(*args):                      # On later calls
        oncall.calls += 1
        print('call %s to %s' % (oncall.calls, func.__name__))
        return func(*args)
    oncall.calls = 0                        # function attribute, locate behind funciton definition
    return oncall



class C:
    @tracer
    def spam(self, a, b, c):
        return a + b + c



if __name__ == '__main__':
    x = C()
    print(x.spam(1, 2, 3))
    print(x.spam('a', 'b', 'c'))
