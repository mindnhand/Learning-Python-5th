#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 sumtree2.py
# Description: without recursive function call
#              but convert to queue or stack
#------------------------------------------


'''
It sometimes helps to understand that internally, Python implements recursion by
pushing information on a call stack at each recursive call, so it remembers where it must
return and continue later. In fact, it's generally possible to implement recursive-style
procedures without recursive calls, by using an explicit stack or queue of your own to
keep track of remaining steps.
'''

def sumtree1(seq):                   # Breadth-first, explict queue
    tot = 0
    items = list(seq)                # Start with copy of top level
    while items:
        print(items)
        front = items.pop(0)
        if not isinstance(front, list):
            tot += front
        else:
            items.extend(front)
    return tot


'''
Technically, this code traverses the list in breadth-first fashion by levels, because it adds
nested lists' contents to the end of the list, forming a first-in-first-out queue. To emulate
the traversal of the recursive call version more closely, we can change it to perform
depth-first traversal simply by adding the content of nested lists to the front of the list,
forming a last-in-first-out stack:
'''

def sumtree2(seq):                  # Depth-first, explicit stack
    tot = 0
    items = list(seq)               # Start with copy of top level
    while items:
        print(items)
        front = items.pop(0)        # Fetch/delete front item
        if not isinstance(front, list):
            tot += front
        else:
            items[:0] = front
    return tot



#-------------------------------test----------------------------------
seq_lst = [1, [2, [3, 4], 5], 6, [7, 8]]     # Arbitrary nesting structure
sum_res1 = sumtree1(seq_lst)                   # sum_res1 is 36
print('The sum result of %s is %s' % (seq_lst, sum_res1))


# Pathological cases
print(sumtree1([1, [2, [3, [4, [5]]]]]))      # Prints 15 (right-heavy)
print(sumtree1([[[[[1], 2], 3], 4], 5]))      # Prints 15 (left-heavy)


print()
print('another test')

sum_res2 = sumtree2(seq_lst)                   # sum_res1 is 36
print('The sum result of %s is %s' % (seq_lst, sum_res2))


# Pathological cases
print(sumtree2([1, [2, [3, [4, [5]]]]]))      # Prints 15 (right-heavy)
print(sumtree2([[[[[1], 2], 3], 4], 5]))      # Prints 15 (left-heavy)
