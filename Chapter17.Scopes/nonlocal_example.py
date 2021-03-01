#!/usr/bin/env python3
#encoding=utf-8



#-----------------------------------------
#
#-----------------------------------------



# normal scope lookup rules, without state modification
def tester(start):
    state = start
    def nested(label):
        print(label, state)
    return nested

f = tester(0)

print('Call tester function: ')
f('spam')
f('ham')
print()


# but if you try to modify state, it will wrong
def tester_modify_wrong(start):
    state = start
    def nested(label):
        print(label, state)
        state += 1
    return nested

try:
    f1 = tester_modify_wrong(0)
    
    print('Call tester_modify_wrong function: ')
    f1('spam')
    f1('ham')
    print()
except Exception as E:
    print(E)
    print()


# use nonlocal to modify the state in the outer def statement block, it will work
def tester_modify_normal(start):
    '''
    As usual with enclosing scope references, we can call the tester factory (closure) function
    multiple times to get multiple copies of its state in memory. The state object in
    the enclosing scope is essentially attached to the nested function object returned; each
    call makes a new, distinct state object, such that updating one function's state wonn't
    impact the other.
    In this sense, Python's nonlocals are more functional than function locals typical in
    some other languages: in a closure function, nonlocals are per-call, multiple copy data.
    '''
    state = start
    def nested(label):
        nonlocal state
        print(label, state)
        state += 1
    return nested

f2 = tester_modify_normal(0)
g1 = tester_modify_normal(42)

print('Call tester_modify_normal function: ')
f2('spam')
f2('ham')
f2('egg')
g1('spam')
g1('ham')
g1('egg')
f2('apple')
print()
