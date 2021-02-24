#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------
# Usage: python3 interactive_loop_try.py
# Description: interactive loop for 
#              while and if statement
#------------------------------------


while True:
    reply = input('Enter text:')
    if reply == 'stop': 
        break
    try:
        num = int(reply)
    except:
        print('Bad!' * 8)
    else:
        print(int(reply)**2)

print('Bye!')
