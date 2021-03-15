#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 squares_nonyield.py
# Description: multiple scan with __iter__
#-------------------------------------------------



class Squares:
    def __init__(self, start, stop):                        # Non-yield generator
        self.start = start                                  # Multiscans: extra object
        self.stop = stop
    def __iter__(self):
        return SquaresIter(self.start, self.stop)


class SquaresIter:
    def __init__(self, start, stop):
        self.value = start - 1
        self.stop = stop
    def __next__(self):
        if self.value == self.stop:
            raise StopIteration
        self.value += 1
        return self.value ** 2



if __name__ == '__main__':
    print('=' * 20 + 'Test for multiple scan')
    S1 = Squares(1, 5)
    for i in S1:
        print(i, end=' ')
    else:
        print()
    print()

    print('=' * 20 + 'Test for multiple scan with next')
    I = iter(S1)
    J = iter(S1)
    print('next(I) next(I) is ', next(I), next(I))          # multiple scan, every iterator has an independent state
    print('next(J) next(J) is ', next(J), next(J))
    print()
    
    print('=' * 20 + 'Test for multiple scan with for loop')
    for i in S1:
        for j in S1:
            print('%s:%s' % (i ,j), end=' ')
    else:
        print()
    
    print()
