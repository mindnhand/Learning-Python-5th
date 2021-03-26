# Extending Built-in Types
Besides implementing new kinds of objects, classes are sometimes used to extend the functionality of Python's built-in types to support more exotic data structures. For instance, to add queue insert and delete methods to lists, you can code classes that wrap (embed) a list object and export insert and delete methods that process the list specially, like the delegation technique we studied in Chapter 31. As of Python 2.2, you can also use inheritance to specialize built-in types. The next two sections show both techniques in action.

## Extending Types by Embedding
Do you remember those set functions we wrote in Chapter 16 and Chapter 18? Here's what they look like brought back to life as a Python class. The following example (the file setwrapper.py) implements a new set object type by moving some of the set functions to methods and adding some basic operator overloading. For the most part, this class just wraps a Python list with extra set operations. But because it's a class, it also supports multiple instances and customization by inheritance in subclasses. Unlike our earlier functions, using classes here allows us to make multiple self-contained set objects with preset data and behavior, rather than passing lists into functions manually:
> 
> > ```python
> > class Set:
> >     def __init__(self, value = []): 		# Constructor
> >         self.data = [] 			# Manages a list
> >         self.concat(value)
> > 
> >     def intersect(self, other): # other is any sequence
> >         res = [] 				# self is the subject
> >         for x in self.data:
> >             if x in other: 		# Pick common items
> >                 res.append(x)
> >         return Set(res) 		# Return a new Set
> > 
> >     def union(self, other): 	# other is any sequence
> >         res = self.data[:] 		# Copy of my list
> >         for x in other: 		# Add items in other
> >             if not x in res:
> >                 res.append(x)
> >         return Set(res)
> > 
> >     def concat(self, value): 	# value: list, Set...
> >         for x in value: 		# Removes duplicates
> >             if not x in self.data:
> >                 self.data.append(x)
> > 
> >     def __len__(self): return len(self.data) 				 	# len(self), if self
> >     def __getitem__(self, id_sli): return self.data[id_sli]  	# self[i], self[i:j]
> >     def __and__(self, other): return self.intersect(other) 		# self & other
> >     def __or__(self, other): return self.union(other) 			# self | other
> >     def __repr__(self): return 'Set:' + repr(self.data) 		# print(self),...
> >     def __iter__(self): return iter(self.data) 					# for x in self,...
> > ```
> 
> To use this class, we make instances, call methods, and run defined operators as usual:
> 
> > ```python
> > from setwrapper import Set
> > x = Set([1, 3, 5, 7])
> > print(x.union(Set([1, 4, 7]))) 		# prints Set:[1, 3, 5, 7, 4]
> > print(x | Set([1, 4, 6])) 			# prints Set:[1, 3, 5, 7, 4, 6]
> > print(x[1:4])
> > ```
> 
Overloading operations such as indexing and iteration also enables instances of our Set class to often masquerade as real lists. Because you will interact with and extend this class in an exercise at the end of this chapter, I won't say much more about this code until Appendix D.

## Extending Types by Subclassing
Beginning with Python 2.2, all the built-in types in the language can now be subclassed directly. Type-conversion functions such as list, str, dict, and tuple have become built-in type names -- although transparent to your script, a type-conversion call (e.g., list('spam')) is now really an invocation of a type's object constructor. 

This change allows you to customize or extend the behavior of built-in types with userdefined class statements: simply subclass the new type names to customize them. Instances of your type subclasses can generally be used anywhere that the original builtin type can appear. For example, suppose you have trouble getting used to the fact that Python list offsets begin at 0 instead of 1. Not to worry -- you can always code your own subclass that customizes this core behavior of lists. The file typesubclass.py shows how:
> 
> > ```python
> > # Subclass built-in list type/class
> > # Map 1..N to 0..N-1; call back to built-in version.
> > class MyList(list):
> >     def __getitem__(self, offset):
> >         print('(indexing %s at %s)' % (self, offset))
> >         return list.__getitem__(self, offset - 1)
> > 
> > if __name__ == '__main__':
> >     print(list('abc'))
> >     x = MyList('abc') 				# __init__ inherited from list
> >     print(x) 						# __repr__ inherited from list
> >     print(x[1]) 					# MyList.__getitem__
> >     print(x[3]) 					# Customizes list superclass method
> >     x.append('spam'); print(x) 		# Attributes from list superclass
> >     x.reverse(); print(x)
> > ```
> 
> In this file, the MyList subclass extends the built-in list's \_\_getitem\_\_ indexing method only, to map indexes 1 to N back to the required 0 to N−1. All it really does is decrement the submitted index and call back to the superclass's version of indexing, but it's enough to do the trick:
> 
> > ```powershell
> > % python typesubclass.py
> > ['a', 'b', 'c']
> > ['a', 'b', 'c']
> > (indexing ['a', 'b', 'c'] at 1)
> > a
> > (indexing ['a', 'b', 'c'] at 3)
> > c
> > ['a', 'b', 'c', 'spam']
> > ['spam', 'c', 'b', 'a']
> > ```
>

This output also includes tracing text the class prints on indexing. Of course, whether changing indexing this way is a good idea in general is another issue -- users of your MyList class may very well be confused by such a core departure from Python sequence behavior! The ability to customize built-in types this way can be a powerful asset, though.

For instance, this coding pattern gives rise to an alternative way to code a set -- as a subclass of the built-in list type, rather than a standalone class that manages an embedded list object as shown in the prior section. As we learned in Chapter 5, Python today comes with a powerful built-in set object, along with literal and comprehension syntax for making new sets. Coding one yourself, though, is still a great way to learn about type subclassing in general.

The following class, coded in the file setsubclass.py, customizes lists to add just methods and operators related to set processing. Because all other behavior is inherited from the built-in list superclass, this makes for a shorter and simpler alternative -- everything not defined here is routed to list directly:
> 
> > ```python
> > from __future__ import print_function 				# 2.X compatibility
> > class Set(list):
> >     def __init__(self, value = []): 				# Constructor
> >         list.__init__([]) 							# Customizes list
> >         self.concat(value) 							# Copies mutable defaults
> > 
> >     def intersect(self, other):           			# other is any sequence
> >         res = [] 									# self is the subject
> >         for x in self:
> >             if x in other: 							# Pick common items
> >                 res.append(x)
> >         return Set(res) 							# Return a new Set
> > 
> >     def union(self, other): 						# other is any sequence
> >         res = Set(self) 							# Copy me and my list
> >         res.concat(other)
> >         return res
> > 
> >     def concat(self, value): 						# value: list, Set, etc.
> >         for x in value: 							# Removes duplicates
> >             if not x in self:
> >                 self.append(x)
> > 
> >     def __and__(self, other): return self.intersect(other)
> >     def __or__(self, other): return self.union(other)
> >     def __repr__(self): return 'Set:' + list.__repr__(self)
> > 
> > if __name__ == '__main__':
> >     x = Set([1,3,5,7])
> >     y = Set([2,1,4,5,6])
> >     print(x, y, len(x))
> >     print(x.intersect(y), y.union(x))
> >     print(x & y, x | y)
> >     x.reverse(); print(x)
> > ```
> 
> Here is the output of the self-test code at the end of this file. Because subclassing core types is a somewhat advanced feature with a limited target audience, I'll omit further details here, but I invite you to trace through these results in the code to study its behavior (which is the same on Python 3.X and 2.X):
> 
> > ```python
> > % python setsubclass.py
> > Set:[1, 3, 5, 7] Set:[2, 1, 4, 5, 6] 4
> > Set:[1, 5] Set:[2, 1, 4, 5, 6, 3, 7]
> > Set:[1, 5] Set:[1, 3, 5, 7, 2, 4, 6]
> > Set:[7, 5, 3, 1]
> > ```
> 

There are more efficient ways to implement sets with dictionaries in Python, which replace the nested linear search scans in the set implementations shown here with more direct dictionary index operations (hashing) and so run much quicker. For more details, see the continuation of this thread in the follow-up book Programming Python. Again, if you're interested in sets, also take another look at the set object type we explored in Chapter 5; this type provides extensive set operations as built-in tools. Set implementations are fun to experiment with, but they are no longer strictly required in Python today.

For another type subclassing example, explore the implementation of the bool type in Python 2.3 and later. As mentioned earlier in the book, bool is a subclass of int with two instances (True and False) that behave like the integers 1 and 0 but inherit custom string-representation methods that display their names.  

