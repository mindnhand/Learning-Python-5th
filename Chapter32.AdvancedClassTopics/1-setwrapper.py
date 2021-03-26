#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------
# Usage: python3 setwrapper.py
# Description: Extending Types by Embedding
#------------------------------------------------------



class Set:
    def __init__(self, value = []): 		# Constructor
        self.data = [] 			# Manages a list
        self.concat(value)

    def intersect(self, other): # other is any sequence
        res = [] 				# self is the subject
        for x in self.data:
            if x in other: 		# Pick common items
                res.append(x)
        return Set(res) 		# Return a new Set

    def union(self, other): 	# other is any sequence
        res = self.data[:] 		# Copy of my list
        for x in other: 		# Add items in other
            if not x in res:
                res.append(x)
        return Set(res)

    def concat(self, value): 	# value: list, Set...
        for x in value: 		# Removes duplicates
            if not x in self.data:
                self.data.append(x)

    def __len__(self): return len(self.data) 				 	# len(self), if self
    def __getitem__(self, id_sli): return self.data[id_sli] 		 	# self[i], self[i:j]
    def __and__(self, other): return self.intersect(other) 		# self & other
    def __or__(self, other): return self.union(other) 			# self | other
    def __repr__(self): return 'Set:' + repr(self.data) 		# print(self),...
    def __iter__(self): return iter(self.data) 					# for x in self,...




if __name__ == '__main__':
    from setwrapper import Set
    x = Set([1, 3, 5, 7])
    print(x.union(Set([1, 4, 7]))) 		# prints Set:[1, 3, 5, 7, 4]
    print(x | Set([1, 4, 6])) 			# prints Set:[1, 3, 5, 7, 4, 6]
    print(x[1:4])
