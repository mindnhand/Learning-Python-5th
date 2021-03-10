#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 first_class_example.py
# Description: the first class example
#-----------------------------------------



class FirstClass:                           # Define a class object
    def setdata(self, value):               # Define class's methods
        self.data = value                   # self is the instance of FirstClass
    def display(self):
        print(self.data)                    # self.data: per instance




if __name__ == '__main__':
    x = FirstClass()                            # Make two instances
    y = FirstClass()                            # Each is a new namespace
    
    
    x.setdata('King Arthur')                    # Call methods: self is x
    y.setdata(3.14159)                          # Runs: FirstClass.setdata(y, 3.14159)
    
    
    
    x.display()                                 # self.data differs in each instance
    y.display()                                 # Runs: FirstClass.display(y)
    
    print('set self.data directly')
    
    x.data = 'New Value'                        # Can get/set attributes
    x.display()                                 # Outside the class too
