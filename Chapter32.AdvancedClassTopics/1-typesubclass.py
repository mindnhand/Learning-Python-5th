#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage: python3 typesubclass.py
# Description: Extending Types by Subclassing
#              Subclass built-in list type/class
#              Map 1..N to 0..N-1; call back to built-in version.
#--------------------------------------------------


class MyList(list):
    def __getitem__(self, offset):
        print('(indexing %s at %s)' % (self, offset))
        return list.__getitem__(self, offset - 1)


if __name__ == '__main__':
    print(list('abc'))
    x = MyList('abc') 			# __init__ inherited from list
    print(x) 				# __repr__ inherited from list
    print(x[1]) 			# MyList.__getitem__
    print(x[3]) 			# Customizes list superclass method
    print(x[0])
    x.append('spam'); print(x) 		# Attributes from list superclass
    x.reverse(); print(x)
    print(dir(x))
