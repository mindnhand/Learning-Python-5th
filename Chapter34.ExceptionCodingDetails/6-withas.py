#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 6-withas.py
# Description: defines a context manager object that traces the entry and 
#              exit of the with block in any with statement it is used for
#---------------------------------------------



class TraceBlock:
    def message(self, arg):
        print('running ' + arg)

    def __enter__(self):
        print('__enter__ method is called: starting with block')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            print('__exit__ method is called: exited normally\n')
        else:
            print('__exit__ method is called: raise an exception!' + str(exc_type))
            #print('exc_value is %s' % exc_value)
            #print('exc_tb is %s' % exc_tb)
            return False            # Propagate




if __name__ == '__main__':
    with TraceBlock() as action:
        action.message('test 1')
        print('reached')

    with TraceBlock() as action:
        action.message('test 2')
        raise TypeError
        print('Not reached')

    '''
    results:
    Chapter34.ExceptionCodingDetails]# python3 6-withas.py
    __enter__ method is called: starting with block
    running test 1
    reached
    __exit__ method is called: exited normally

    __enter__ method is called: starting with block
    running test 2
    __exit__ method is called: raise an exception!<class 'TypeError'>
    Traceback (most recent call last):
      File "6-withas.py", line 38, in <module>
          raise TypeError
          TypeError
    '''
