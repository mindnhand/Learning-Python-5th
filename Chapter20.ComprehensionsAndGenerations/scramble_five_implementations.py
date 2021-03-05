#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 five_implementations.py
# Description: Five Implementations to scramble sequence
#---------------------------------------------------



# 1. Normal Function
def scramble_func(seq):
    res = []
    for i in range(len(seq)):
        res.append(seq[i:] + seq[:i])
    return res


scram_res_func = scramble_func('spam')

print('=' * 20 + 'Normal Function' + '=' * 20)
print(scram_res_func)


# 2. List Comprehension
def scramble_comp(seq):
    return [seq[i:] + seq[:i] for i in range(len(seq))]

scram_res_comp = scramble_comp('spam')

print('=' * 20 + 'List Comprehension' + '=' * 20)
print(scram_res_comp)


# 3. Generator Function
def scramble_gene_func(seq):
    for i in range(len(seq)):
        yield seq[i:] + seq[:i]

scramble_res_gene_func = scramble_gene_func('spam')

print('=' * 20 + 'Generator Function' + '=' * 20)
print(list(scramble_res_gene_func))



# 4. Generator Expression
'''
Notice that we can't use the assignment statement of the first generator expression version here,
because generator expressions cannot contain statements. This makes them a bit narrower 
in scope; in many cases, though, expressions can do similar work, as shown here.
'''
seq = 'spam'
G = (seq[i:] + seq[:i] for i in range(len(seq)))

print('=' * 20 + 'Generator Expression' + '=' * 20)
print(list(G))



# 5. Lambda and Generator Expression
'''
To generalize a generator expression for an arbitrary subject, wrap it in a simple
function that takes an argument and returns a generator that uses it:
'''
F = lambda seq: (seq[i:] + seq[:i] for i in range(len(seq)))        # 如果lambda seq:后面的部分不用小括号括起来，则会报错

lambda_res = F('spam')
print('=' * 20 + 'lambda Generator Expression' + '=' * 20)
print(list(lambda_res))
