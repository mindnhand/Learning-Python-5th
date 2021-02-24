#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------
# Usage: python3 interactive_loop_try-1.py
# Description: interactive loop for 
#              while and if statement
#------------------------------------


while True:
    reply = input('Enter text:')
    if reply == 'stop': 
        break
    try:
        print(int(reply) ** 2)
    except:
        print('Bad!' * 8)

print('Bye!')
