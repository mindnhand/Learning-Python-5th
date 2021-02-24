#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------
# Usage: python3 interactive_loop.py
# Description: interactive loop for 
#              while and if statement
#------------------------------------


while True:
    reply = input('Enter text:')
    if reply == 'stop': break
    print(reply.upper())
