#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------
# Usage: 
# Description: 
#-----------------------------------------------------



'''
However, generators can be better in terms of both memory use and performance in
larger programs. They allow functions to avoid doing all the work up front, which is
especially useful when the result lists are large or when it takes a lot of computation to
produce each value. Generators distribute the time required to produce the series of
values among loop iterations.
'''


# 1. normal function
def buildsquares(n):
    res_lst = []
    for i in range(n):
        res_lst.append(i ** 2)
    return res_lst


print('=' * 20 + 'test for normal function' + '=' * 20)
res_lst = buildsquares(5)
for res in res_lst:
    print(res, end=':')
else:
    print()



# 2. list comprehension
print('=' * 20 + 'test for list comprehension' + '=' * 20)
res_comp = [x ** 2 for x in range(5)]
for res in res_comp:
    print(res, end=':')
else:
    print()


# 3. map-lambda
print('=' * 20 + 'test for map-lambda' + '=' * 20)
map_obj = map(lambda x: x ** 2, range(5))
for m in map_obj:
    print(m, end=':')
else:
    print()


# 4. generator function
def ups(line):
    for sub in line.split(','):
        yield sub.upper()

print('=' * 20 + 'test for generator function' + '=' * 20)
gen_up = ups('aaa, bbb, ccc')
print('the result of %s is %s' % (gen_up, list(gen_up)))            # 单次使用，遍历完即空

gen_up = ups('aaa, bbb, ccc')                                       # 再次使用需要重新生成
dict_comp = {i: s for (i, s) in enumerate(gen_up)}
print('dict_comprehension result is %s' % dict_comp)
