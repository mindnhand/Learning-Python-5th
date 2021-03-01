#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 global_single_state.py
# Description: with global, single state be retained
#----------------------------------------------



# with globla, can retain single state
def tester(start):
    '''
    This works in this case, but it requires global declarations in both functions and is
    prone to name collisions in the global scope (what if state is already being used?). A
    worse, and more subtle, problem is that it only allows for a single shared copy of the
    state information in the module scope—if we call tester again, we’ll wind up resetting
    the module's tate variable, such that prior calls will see their state overwritten
    When you are using nonlocal and nested function closures instead of
    global, each call to tester remembers its own unique copy of the state object.
    '''
    global state                    # Move it to the module to change it
    state = start                   # global allows changes in module scope
    def nested(label):
        global state
        print(label, state)
        state += 1
    return nested


F = tester(0)
F('spam')                           # Each call increments shared global state
F('egg')

G = tester(42)                      # Reset state's single copy in global scope
G('toast')
G('bacon')
F('ham')                            # will print 44
