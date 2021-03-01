#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------
# Usage: python3 across_file_2nd.py
# Description: test across file change
#--------------------------------------


import across_file_1st as first


print('before modification: x = %s' % first.x)


first.set_x(88)
print('after modification: x = %s' % first.x)
