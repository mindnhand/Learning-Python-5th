#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage: python3 permute.py
# Description: Two implementation of Permutation
#--------------------------------------------------


'''
Permutations produce more orderings than the original shuffler -- for N items, we get
N! (factorial) results instead of just N (24 for 4: 4 * 3 * 2 * 1). In fact, that's why we need
recursion here: the number of nested loops is arbitrary, and depends on the length of
the sequence permuted.
but some programs warrant the more exhaustive set of all possible orderings 
we get from permutations -- produced using recursive functions in both 
list-builder and generator forms by the following module file:
'''

import math
import timeit


def permute1(seq):
    if not seq:                             # Shuffle sequence: string, list, set, not for dict
        return [seq]
    else:                               # for string, don't convert
        if not isinstance(seq, str):        # convert list, set to string
            seq = ''.join(str(x) for x in seq)
        res = []
        for i in range(len(seq)):
            rest = seq[:i] + seq[i+1:]      # Delete current node
            for x in permute1(rest):        # Permute the other nodes
                res.append(seq[i] + x)      # Add current at front
        return res


def permute2(seq):
    if not seq:                             # Shuffle sequence: generator, not for dict
        yield seq                           # Empty sequence
    else:
        if not isinstance(seq, str):
            seq = ''.join(str(x) for x in seq)
        for i in range(len(seq)):     
            rest = seq[:i] + seq[i+1:]      # Delete current node
            for x in permute2(rest):      # Permute the others
                yield seq[i] + x            # Add current node at front

if __name__ == '__main__':

    print('=' * 20 + 'test for permute1' + '=' * 20)
    s1 = 'abc'
    '''
    有6组合方式：
        第一个位置有3种可能（可以是a, b, c三者中任意一个）；
        第二个位置有2种可能（是其第一个位置确定之后剩下的两个字母中任意一个）；
        第三个位置有1种可能（是前两个位置确定之后剩下的唯一一个字母）。
        所以，最终的组合数为3x2x1=6
    '''
    r1_1 = permute1(s1)
    
    
    s2 = 'spam'
    '''
    有24种组合方式：
        第一个位置有4种可能（可以是s, p, a, m四个中的任意一个）；
        第二个位置有3种可能（可以是第一个位置确定之后剩下的3个字母中的任意一个）；
        第三个位置有2种可能（可以是前两个位置确定之后剩下的2个字母种的任意一个）；
        第四个位置有1种可能（就是前3个位置确定之后剩下的唯一一个字母）。
        所以，最终的组合数为4x3x2x1=24
    '''
    r1_2 = permute1(s2)
    
    print(r1_1)
    print(r1_2)
    
    
    
    print('=' * 20 + 'test for permute2' + '=' * 20)
    r2_1 = permute2(s1)
    r2_2 = permute2(s2)
    
    print(list(r2_1))
    print(list(r2_2))
    
    
    
    
    '''
    Since the number of combinations is a factorial that explodes exponentially, 
    the preceding permute1 recursive list-builder function will either introduce 
    a noticeable and perhaps interminable pause or fail completely due to memory requirements, 
    whereas the permute2 recursive generator will not—it returns each individual result quickly, a
    nd can handle very large result sets:
    '''
    
    print('=' * 20 + 'test for timeit' + '=' * 20)
    
    
    facto_res = math.factorial(10)
    stmts = '''
math.factorial(10)
    '''
    facto_secs = timeit.timeit(stmt=stmts, setup='import math')
    print('facto_secs = %s' % facto_secs)
    
    seq = list(range(10))
    
    p1_secs = timeit.timeit(stmt='seq = list(range(10)); permute1(seq)', setup='from __main__ import permute1', number=1)  # number=1000000，如果不改为1，就需要执行很久很久
    print('p1_secs = %s' % p1_secs)
    p2_secs = timeit.timeit(stmt='seq = list(range(10)); permute2(seq)', setup='from __main__ import permute2', number=1)
    print('p2_secs = %s' % p2_secs)
    '''
    python3 permute.py                                                                       
    ====================test for permute1====================
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    ['spam', 'spma', 'sapm', 'samp', 'smpa', 'smap', 'psam', 'psma', 'pasm', 'pams', 'pmsa', 'pmas', 'aspm', 'asmp', 'apsm', 'apms', 'amsp', 'amps',
    'mspa', 'msap', 'mpsa', 'mpas', 'masp', 'maps']
    ====================test for permute2====================
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    ['spam', 'spma', 'sapm', 'samp', 'smpa', 'smap', 'psam', 'psma', 'pasm', 'pams', 'pmsa', 'pmas', 'aspm', 'asmp', 'apsm', 'apms', 'amsp', 'amps',
    'mspa', 'msap', 'mpsa', 'mpas', 'masp', 'maps']
    ====================test for timeit====================
    facto_secs = 0.16772253601811826
    p1_secs = 14.951015113969333
    p2_secs = 7.909955456852913e-06
    '''
    p2_secs = timeit.timeit(stmt='seq = list(range(50)); permute2(seq)', setup='from __main__ import permute2', number=1)
    print('p2_secs = %s' % p2_secs)
    print('p2_lth = %s' % len(list(permute2(list(range(50))))))

    # range(50)的时候，下面这种方式需要执行很久，而且消耗了20G内存还未计算完成
    #p1_secs = timeit.timeit(stmt='seq = list(range(50)); permute1(seq)', setup='from __main__ import permute1', number=1)  # number=1000000，如果不改为1，就需要执行很久很久
    #print('p1_secs = %s' % p1_secs)
