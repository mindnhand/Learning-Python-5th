#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------
# Usage: python3 6-super.py
# Description: As briefly noted in Python's library manual, super also doesn't fully 
#              work in the presence of \_\_X\_\_ operator overloading methods. If you
#              study the following code, you'll see that direct named calls to overload 
#              methods in the superclass operate normally, but using the super result 
#              in an expression fails to dispatch to the superclass's overload method
#-------------------------------------


class C:
    def __getitem__(self, idx):             # Indexing overload method
        print('C index')


class D(C):
    def __getitem__(self, idx):             # Redefine __getitem__ method
        print('D index')
        C.__getitem__(self, idx)            # Traditional call from works
        super().__getitem__(idx)            # Direct name calls work too
        super()[idx]                        # But operator don't! it call __getattribute__ method


if __name__ == '__main__':
    x = C()
    print(x[99])
    print()

    y = D()
    print(y[99])
