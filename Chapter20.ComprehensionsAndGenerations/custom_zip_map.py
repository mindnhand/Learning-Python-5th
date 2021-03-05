#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage: python3 custom_zip_map.py
# Description: myzip with pad
#--------------------------------------------------



# 1. while loop and list
def myzip_while(*seqs):
    seqs = [list(s) for s in seqs]
    res = []
    while all(seqs):
        res.append(tuple(s.pop(0) for s in seqs))
    return res


def myzip_while_pad(*seqs, pad=None):
    seqs = [list(s) for s in seqs]
    res = []
    while any(seqs):
        res.append(tuple((s.pop(0) if s else pad) for s in seqs))
    return res


print('=' * 20 + 'while loop and list' + '=' * 20)
s1, s2 = 'abc', 'xyz123'
print(myzip_while(s1, s2))
print(myzip_while_pad(s1, s2))
print(myzip_while_pad(s1, s2, pad=99))



# 2. generator function
def myzip_gene_func(*seqs):
    seqs = [list(s) for s in seqs]
    while all(seqs):
        yield tuple(s.pop(0) for s in seqs)


def myzip_gene_func_pad(*seqs, pad=None):
    seqs = [list(s) for s in seqs]
    while any(seqs):
        yield tuple((s.pop(0) if s else pad) for s in seqs)


print('=' * 20 + 'generator function' + '=' * 20)
s1, s2 = 'abc', 'xyz123'
print(list(myzip_gene_func(s1, s2)))
print(list(myzip_gene_func_pad(s1, s2)))
print(list(myzip_gene_func_pad(s1, s2, pad=99)))



# 3. with length
def myzip_lth(*seqs):
    minlen = min(len(s) for s in seqs)
    return [tuple((s[i]) for s in seqs) for i in range(minlen)]

def myzip_lth_pad(*seqs, pad=None):
    maxlen = max(len(s) for s in seqs)
    idx = range(maxlen)
    return [tuple((s[i] if len(s) > i else pad) for s in seqs) for i in idx]



print('=' * 20 + 'with length' + '=' * 20)
s1, s2 = 'abc', 'xyz123'
print(myzip_lth(s1, s2))
print(myzip_lth_pad(s1, s2))
print(myzip_lth_pad(s1, s2, pad=99))



# 4. generator expression
def myzip_gene_expr(*seqs):
    minlen = min(len(s) for s in seqs)
    return (tuple(s[i] for s in seqs) for i in range(minlen))

def myzip_gene_expr_pad(*seqs, pad=None):
    maxlen = max(len(s) for s in seqs)
    idx = range(maxlen)
    return (tuple(s[i] if len(s) > i else pad for s in seqs) for i in idx)


print('=' * 20 + 'generator expression' + '=' * 20)
s1, s2 = 'abc', 'xyz123'
print(list(myzip_gene_expr(s1, s2)))
print(list(myzip_gene_expr_pad(s1, s2)))
print(list(myzip_gene_expr_pad(s1, s2, pad=99)))
