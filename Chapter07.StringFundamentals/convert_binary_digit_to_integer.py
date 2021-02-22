#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------------------
# Usage: python3 convert_binary_digit_to_integer.py binary_digit
# Description: 将二进制输入参数转换为十进制数并打印到标准输出
#---------------------------------------------------------------


import sys

'''
execution result in command line:
~]# python3 convert_binary_digit_to_integer.py 101110
binary digit -> integer: 46
~]# python3 convert_binary_digit_to_integer.py 101111
binary digit -> integer: 47
'''

input_binary = sys.argv[1]
integer = 0

while input_binary != '':
    integer = integer * 2 + (ord(input_binary[0]) - ord('0'))
    input_binary = input_binary[1:]

print('binary digit -> integer: %d' % integer)
