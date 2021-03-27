#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------
# Usage: python3 2-try_finally.py
# Description: try-finally to do some cleanup jobs
#---------------------------------------



'''
When the function in this code raises its exception, the control flow jumps 
back and runs the finally block to close the file. The exception is then 
propagated on to either another try or the default top-level handler, which 
prints the standard error message and shuts down the program. Hence, the 
statement after this try is never reached. If the function here did not raise 
an exception, the program would still execute the finally block to close the 
file, but it would then continue below the entire try statement.
'''


class MyError(Exception):
    pass


def stuff(file):
    raise MyError('raise an Exception in stuff(file) function')


file = open('data', 'w')            # Open an output file (this can fail too)


try:
    stuff(file)                     # Raises exception
finally:
    file.close()                    # Always close file to flush output buffers

print('Not reached')                # Continue here only if no exceptions
