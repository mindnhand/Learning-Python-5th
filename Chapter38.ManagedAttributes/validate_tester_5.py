#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 5-validate_tester.py validate_properties-5
# Description: test for validate_properties-5.py
#------------------------------------------------




from __future__ import print_function 			# 2.X

def loadclass():
    import sys, importlib
    modulename = sys.argv[1] 				# Module name in command line
    module = importlib.import_module(modulename) 	# Import module by name string
    print('[Using: %s]' % module.CardHolder) 		# No need for getattr() here
    return module.CardHolder

def printholder(who):
    print(who.acct, who.name, who.age, who.remain, who.addr, sep=' / ')



if __name__ == '__main__':
    CardHolder = loadclass()
    print('1. initialize instance bob')
    bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')

    print('\n2. print instance bob')
    printholder(bob)

    print("\n3. set bob's name")
    bob.name = 'Bob Q. Smith'

    print("\n4. set bob's age")
    bob.age = 50

    print("\n5. set bob's acct")
    bob.acct = '23-45-67-89'

    print('\n6. print instance bob')
    printholder(bob)

    print()
    print('=' * 40)
    print()

    print('7. initialize instance sue')
    sue = CardHolder('5678-12-34', 'Sue Jones', 35, '124 main st')

    print('\n8. print instance sue')
    printholder(sue)
    try:
        sue.age = 200
    except:
        print('Bad age for Sue')
    try:
        sue.remain = 5
    except:
        print("Can't set sue.remain")
    try:
        sue.acct = '1234567'
    except:
        print('Bad acct for Sue')

    '''
    result:
    Chapter38.ManagedAttributes]# python3 5-validate_tester.py validate_properties-5
    [Using: <class '5-validate_properties.CardHolder'>]
    12345*** / bob_smith / 40 / 19.5 / 123 main st
    23456*** / bob_q._smith / 50 / 9.5 / 123 main st
    56781*** / sue_jones / 35 / 24.5 / 124 main st
    Bad age for Sue
    Can't set sue.remain
    Bad acct for Sue
    '''
