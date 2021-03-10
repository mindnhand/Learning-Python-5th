#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 second_class_example.py
# Description: class inherites
#---------------------------------------------------



'''
import first_class_example.FirstClass as FirstClass
这种方式将会导致下面的错误
Traceback (most recent call last):
      File "second_class_example.py", line 12, in <module>
          import first_class_example.FirstClass as FirstClass
          ModuleNotFoundError: No module named 'first_class_example.FirstClass'; 'first_class_example' is not a package
'''
from first_class_example import FirstClass


class SecondClass(FirstClass):                          # Inherits setdata
    def display(self):                                  # Changes display, this will replace the display function defined in FirstClass
        print('Current value = "%s"' % self.data)



if __name__ == '__main__':
    z = SecondClass()
    z.setdata(42)                                           # Finds setdata in FirstClass
    z.display()                                             # Finds overriden method in SecondClass
    #print(dir(z))
