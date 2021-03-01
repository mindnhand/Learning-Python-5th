#!/usr/bin/env python3
#encoding=utf-8



#-------------------------------------------
# Usage: python3 function_attribute_state_retain.py
# Description: function attribute carry out multi-state retain
#-------------------------------------------


# with function attribute, also can carry out multi-state retain
def tester(start):
    '''
    As a portable and often simpler state-retention option, we can also sometimes achieve
    the same effect as nonlocals with function attributes—user-defined names attached to
    functions directly. When you attach user-defined attributes to nested functions generated
    by enclosing factory functions, they can also serve as per-call, multiple copy, and
    writeable state, just like nonlocal scope closures and class attributes.
    Because factory functions make a new function on each call anyhow,
    this does not require extra objects—the new function’s attributes become percall
    state in much the same way as nonlocals, and are similarly associated with the
    generated function in memory.
    Moreover, function attributes allow state variables to be accessed outside the nested
    function, like class attributes; with nonlocal, state variables can be seen directly only
    within the nested def.
    '''
    def nested(label):
        print(label, nested.state)                  # nested is in enclosing scope
        nested.state += 1                           # Changing attr, not nested itself
    nested.state = start                            # Initial state after func defined
    return nested


F = tester(0)
F('spam')                                           # F is a 'nested' with state attached
F('ham')
print('F.state = %s' % F.state)                     # can access state outside functions too


G = tester(42)                                      # G has own state, doesn't overwrite F's
G('eggs')
F('lp')
print('F.state = %s' % F.state)
print('G.state = %s' % G.state)                     # state is accessable and per-call
