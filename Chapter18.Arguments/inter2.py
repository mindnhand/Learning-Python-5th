#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage: python3 inter2.py
# Description: calculate union and intersect 
#--------------------------------------------------



def intersect(*args):
    res = []
    for x in args[0]:                   # Scan first sequence
        if x in res:                    # Skip duplicates
            continue                    
        for other in args[1:]:          # For all other args 
            if x not in other:          # Item in each one? 
                break                   # No: break out of loop
        else:                           # Yes: add item to end
            res.append(x)
    return res


def union(*args):
    res = []
    for seq in args:                    # for all args
        for x in seq:                   # for all nodes
            if x not in res:
                res.append(x)           # add new items to result
    return res


s1 = 'spam'
s2 = 'scam'
s3 = 'slam'

insec_res = intersect(s1, s2)
print('<%s> intersect <%s> is equal to %s' % (s1, s2, insec_res))

union_res = union(s1, s2)
print('<%s> union <%s> is equal to %s' % (s1, s2, union_res))

whole_insec_res = intersect(s1, s2, s3)
print('intersect result of <%s>, <%s>, <%s> is equal to %s' % (s1, s2, s3, whole_insec_res))


print('-' * 20 + 'Seperate Line' + '-' * 20)
print('another thoroughly test')


def tester(func, items, trace=True):
    for i in range(len(items)):
        items = items[1:] + items[:1]
        if trace:
            print(items)
        print(sorted(func(*items)))


print('intersect result: ')
tester(intersect, ('a', 'abcdefg', 'abdst', 'albmcnd'))

print('union result: ')
tester(union, ('a', 'abcdefg', 'abdst', 'albmcnd'), False)

print('another intersect result: ')
tester(intersect, ('ba', 'abcdefg', 'abdst', 'albmcnd'), False)
