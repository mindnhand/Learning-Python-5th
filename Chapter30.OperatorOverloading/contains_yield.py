#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 contains_yield.py
# Description: membership, multiple scan with yield
#-------------------------------------------


'''
Now that you know about yield in iteration methods, you should be able to tell that the 
following is equivalent but allows multiple active scans—and judge for yourself whether i
ts more implicit nature is worth the nested-scan support and six lines shaved (this is in 
file contains_yield.py):
'''


class Iters:
    def __init__(self, value):
        self.data = value
    def __getitem__(self, i):                       # Fallback for iteration
        print('get[%s]: ' % i, end='')              # Also for index, slice
        return self.data[i]
    def __iter__(self):                             # Preferred for iteration
        print('iter=> next: ', end='')              # Allows multiple active iterators
        for x in self.data:                         # no __next__ to alias to next
            yield x
            print('next: ', end='')
    def __contains__(self, x):                      # Preferred for 'in'
        print('contains: ', end='')
        return x in self.data




if __name__ == '__main__':
    X = Iters([1, 2, 3, 4, 5])                          # Make instance
    print(3 in X)                                       # Membership
    for i in X:                                         # for loop
        print(i, end=' | ')
    else:
        print()
        
    print([i ** 2 for i in X])                          # Other iteration contexts
    print(list(map(bin, X)))

    I = iter(X)                                         # Manual iteration (what other contexts do)
    while True:
        try:
            print(next(I), end=' @ ')
        except StopIteration:
            break
    print()
    print(X[1])
    for i in X:
        for j in X:
            print('%s:%s' % (i, j), end=' ')
    else:
        print()

    '''
    On both Python 3.X and 2.X, when either version of this file runs its output is as follows
    —the specific __contains__ intercepts membership, the general __iter__ catches other
    iteration contexts such that __next__ (whether explicitly coded or implied by yield) is
    called repeatedly, and __getitem__ is never called:
    # Result 1:
    [root@localhost Chapter30.OperatorOverloading]# python3 contains_yield.py
    contains: True
    iter=> next: 1 | next: 2 | next: 3 | next: 4 | next: 5 | next:
    iter=> next: next: next: next: next: next: [1, 4, 9, 16, 25]
    iter=> next: next: next: next: next: next: ['0b1', '0b10', '0b11', '0b100', '0b101']                                                            
    iter=> next: 1 @ next: 2 @ next: 3 @ next: 4 @ next: 5 @ next:
    get[1]: 2
    iter=> next: iter=> next: 1:1 next: 1:2 next: 1:3 next: 1:4 next: 1:5 next: next: iter=> next: 2:1 next: 2:2 next: 2:3 next: 2:4 next: 2:5 next:
    next: iter=> next: 3:1 next: 3:2 next: 3:3 next: 3:4 next: 3:5 next: next: iter=> next: 4:1 next: 4:2 next: 4:3 next: 4:4 next: 4:5 next: next: iter=> next: 5:1 next: 5:2 next: 5:3 next: 5:4 next: 5:5 next: next:
    '''

    '''
    Watch what happens to this code's output if we comment out its __contains__ method,
    though—membership is now routed to the general __iter__ instead:
    # Result 2: commented out __contains__ method
    [root@localhost Chapter30.OperatorOverloading]# python3 contains_yield.py
    iter=> next: next: next: True
    iter=> next: 1 | next: 2 | next: 3 | next: 4 | next: 5 | next: 
    iter=> next: next: next: next: next: next: [1, 4, 9, 16, 25]
    iter=> next: next: next: next: next: next: ['0b1', '0b10', '0b11', '0b100', '0b101']
    iter=> next: 1 @ next: 2 @ next: 3 @ next: 4 @ next: 5 @ next: 
    get[1]: 2
    iter=> next: iter=> next: 1:1 next: 1:2 next: 1:3 next: 1:4 next: 1:5 next: next: iter=> next: 2:1 next: 2:2 next: 2:3 next: 2:4 next: 2:5 next: next: iter=> next: 3:1 next: 3:2 next: 3:3 next: 3:4 next: 3:5 next: next: iter=> next: 4:1 next: 4:2 next: 4:3 next: 4:4 next: 4:5 next: next: iter=> next: 5:1 next: 5:2 next: 5:3 next: 5:4 next: 5:5 next: next:
    '''

    '''
    And finally, here is the output if both __contains__ and __iter__ are commented out
    —the indexing __getitem__ fallback is called with successively higher indexes until it
    raises IndexError, for membership and other iteration contexts:
    # Result 3: commented out __contains__ and __iter__ methods
    [root@localhost Chapter30.OperatorOverloading]# python3 contains_yield.py
    get[0]: get[1]: get[2]: True
    get[0]: 1 | get[1]: 2 | get[2]: 3 | get[3]: 4 | get[4]: 5 | get[5]: 
    get[0]: get[1]: get[2]: get[3]: get[4]: get[5]: [1, 4, 9, 16, 25]
    get[0]: get[1]: get[2]: get[3]: get[4]: get[5]: ['0b1', '0b10', '0b11', '0b100', '0b101']
    get[0]: 1 @ get[1]: 2 @ get[2]: 3 @ get[3]: 4 @ get[4]: 5 @ get[5]: 
    get[1]: 2
    get[0]: get[0]: 1:1 get[1]: 1:2 get[2]: 1:3 get[3]: 1:4 get[4]: 1:5 get[5]: get[1]: get[0]: 2:1 get[1]: 2:2 get[2]: 2:3 get[3]: 2:4 get[4]: 2:5 get[5]: get[2]: get[0]: 3:1 get[1]: 3:2 get[2]: 3:3 get[3]: 3:4 get[4]: 3:5 get[5]: get[3]: get[0]: 4:1 get[1]: 4:2 get[2]: 4:3 get[3]: 4:4 get[4]: 4:5 get[5]: get[4]: get[0]: 5:1 get[1]: 5:2 get[2]: 5:3 get[3]: 5:4 get[4]: 5:5 get[5]: get[5]:
    '''

    '''
    As we've seen, the __getitem__ method is even more general: besides iterations, it also
    intercepts explicit indexing as well as slicing. Slice expressions trigger __getitem__ with
    a slice object containing bounds, both for built-in types and user-defined classes, so
    slicing is automatic in our class
    '''
