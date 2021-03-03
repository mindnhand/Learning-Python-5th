#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 recursive_directively_mysum.py
# Description: recursive call, dynamic function build
#              and dynamic function call
#-------------------------------------------------




# method 1: if...else...
def mysum1(seq):
    print(seq)              # Trace recursive levels
    if not seq:             # seq is shorter at each level
        return 0
    else:
        return seq[0] + mysum1(seq[1:])



# method 2: ternary expression
def mysum2(seq):
    return 0 if not seq else seq[0] + mysum2(seq[1:])


# method 3: any type, assume one
def mysum3(seq):
    return seq[0] if len(seq) == 1 else seq[0] + mysum3(seq[1:])


# method 4: 3.x expand assign
def mysum4(seq):
    first, *rest = seq
    return first if not rest else first + mysum4(rest)



#--------------------------------test------------------------------
seq_tup = (1, 2, 3, 4, 5)
for i in range(1, 5):
    sum_method_name = 'mysum' + str(i)
    sum_method = eval(sum_method_name)      # dynamic function build, note: mysum4 != 'mysum4'
    print('test %s: ' % sum_method_name)
    exec('sum_res = sum_method(seq_tup)')   # dynamic function call, return value need to be saved inside the exec
    print('the result of sum is %s' % sum_res)
    print()

#method_tup = (mysum1, mysum2, mysum3, mysum4)
#for meth in method_tup:
#    print('test %s' % meth)
#    exec('sum_res = meth(seq_tup)')
#    print('the result of sum is %s' % sum_res)
#    print()

