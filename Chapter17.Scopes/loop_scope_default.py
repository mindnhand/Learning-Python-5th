#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
#
#------------------------------------------------



# DOES NOT WORK AS RESPECT!  scope in loop, will remember the last loop value, not every loop value
def makeActions():
    '''
    This method will not get the right result
    '''
    acts = []
    for i in range(5):                          # Tries to remember each i
        acts.append(lambda x: i ** x)           # But all remember same last i
    return acts


acts_list = makeActions()
print('Wrong result: --> ', end='')
for n in range(5):
    print(acts_list[n](2), sep=' ', end=' ')                      # tries to calculate the i ** 2, but all value will be the same, 16
else:
    print()


# WORK AS RESPECT! pass default value in the enclosing scope
def makeActionsDefault():
    '''
    with the default argument in lambda, 
    this method will get the right result
    '''
    acts = []
    for i in range(5):                          # Use default instead
        acts.append(lambda x, i=i: i ** x)      # Remember current i 
    return acts

acts_list_default = makeActionsDefault()
print('Right result: --> ', end='')
for nd in range(5):
    print(acts_list_default[nd](2), sep=' ', end=' ')
else:
    print()
