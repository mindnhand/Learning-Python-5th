#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------
# Usage: python3 mymap.py
# Description: 4 implementations mymap
#------------------------------------------------------



# 1. for loop
def mymap_for(func, *seqs):
    res_lst = []
    for args in zip(*seqs):
        res_lst.append(func(*args))
    return res_lst

print('=' * 20 + 'for loop mymap' + '=' * 20)
print(mymap_for(abs, list(range(-2, 3))))
print(mymap_for(pow, [1, 2, 3], [2, 3, 4, 5]))


# 2. list comprehension
def mymap_lst_comp(func, *seqs):
    return [func(*args) for args in zip(*seqs)]

print('=' * 20 + 'for list comprehension' + '=' * 20)
print(mymap_lst_comp(abs, list(range(-2, 3))))
print(mymap_lst_comp(pow, [1, 2, 3], [2, 3, 4, 5]))


# 3. generator function
def mymap_gene_func(func, *seqs):
    for args in zip(*seqs):
        yield func(*args)


print('=' * 20 + 'for generator function' + '=' * 20)
res1 = mymap_gene_func(abs, list(range(-2, 3)))
res2 = mymap_gene_func(pow, [1, 2, 3], [2, 3, 4, 5])
print(list(res1))
print(list(res2))


# 4. generator expression
def mymap_gene_expr(func, *seqs):
    return (func(*args) for args in zip(*seqs))


print('=' * 20 + 'for generator expression' + '=' * 20)
res_expr1 = mymap_gene_expr(abs, list(range(-2, 3)))
res_expr2 = mymap_gene_expr(pow, [1, 2, 3], [2, 3, 4, 5])
print(list(res_expr1))
print(list(res_expr2))

