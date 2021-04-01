from __future__ import print_function 			# 2.X
from validate_tester_5 import loadclass
CardHolder = loadclass()

print('1. initialize instance bob')
bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')

print('\n2. print instance bob')
print('bob:', bob.name, bob.acct, bob.age, bob.addr)

print('\n3. initialize instance sue')
sue = CardHolder('5678-12-34', 'Sue Jones', 35, '124 main st')

print('\n4. print instance sue')
print('sue:', sue.name, sue.acct, sue.age, sue.addr) 		# addr differs: client data

print('\n5. print instance bob')
print('bob:', bob.name, bob.acct, bob.age, bob.addr) 		# name,acct,age overwritten?
