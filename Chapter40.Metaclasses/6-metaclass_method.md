# Metaclass Methods
Just as important as the inheritance of names, methods in metaclasses process their instance classes -- not the normal instance objects we've known as "self," but classes themselves. This makes them similar in spirit and form to the class methods we studied in Chapter 32, though they again are available in the metaclasses instance realm only, not to normal instance inheritance. The failure at the end of the following, for example, stems from the explicit name inheritance rules of the prior section:
> ```python
> >>> class A(type):
>         def x(cls): print('ax', cls) 				# A metaclass (instances=classes)
>         def y(cls): print('ay', cls) 				# y is overridden by instance B
> 
> >>> class B(metaclass=A):
>         def y(self): print('by', self) 			# A normal class (normal instances)
>         def z(self): print('bz', self) 			# Namespace dict holds y and z
> >>> B.x 					# x acquired from metaclass
> <bound method A.x of <class '__main__.B'>>
> >>> B.y 					# y and z defined in class itself
> <function B.y at 0x0295F1E0>
> >>> B.z
> <function B.z at 0x0295F378>
> >>> B.x() 				# Metaclass method call: gets cls
> ax <class '__main__.B'>
> >>> I = B() 				# Instance method calls: get inst
> >>> I.y()
> by <__main__.B object at 0x02963BE0>
> >>> I.z()
> bz <__main__.B object at 0x02963BE0>
> >>> I.x() 				# Instance doesn't see meta names
> AttributeError: 'B' object has no attribute 'x'
> ```

## Metaclass Methods Versus Class Methods
Though they differ in inheritance visibility, much like class methods, metaclass methods are designed to manage class-level data. In fact, their roles can overlap -- much as metaclasses do in general with class decorators -- but metaclass methods are not accessible except through the class, and do not require an explicit classmethod class-level data declaration in order to be bound with the class. In other words, metaclass methods can be thought of as implicit class methods, with limited visibility:
> ```python
> >>> class A(type):
>         def a(cls): 					# Metaclass method: gets class
>             cls.x = cls.y + cls.z
> >>> class B(metaclass=A):
>         y, z = 11, 22
>         @classmethod 					# Class method: gets class
>         def b(cls):
>             return cls.x
> 
> >>> B.a() 				# Call metaclass method; visible to class only
> >>> B.x 					# Creates class data on B, accessible to normal instances
> 33
> >>> I = B()
> >>> I.x, I.y, I.z
> (33, 11, 22)
> >>> I.b() 				# Class method: sends class, not instance; visible to instance
> 33
> >>> I.a() 				# Metaclass methods: accessible through class only
> AttributeError: 'B' object has no attribute 'a'
> ```

## Operator Overloading in Metaclass Methods
Just like normal classes, metaclasses may also employ operator overloading to make built-in operations applicable to their instance classes. The \_\_getitem\_\_ indexing method in the following metaclass, for example, is a metaclass method designed to process classes themselves -- the classes that are instances of the metaclass, not those classes' own later instances. In fact, per the inheritance algorithms sketched earlier, normal class instances don't inherit names acquired via the metaclass instance relationship at all, though they can access names present on their own classes:
> ```python
> >>> class A(type):
>         def __getitem__(cls, i): 				# Meta method for processing classes:
>             return cls.data[i] 				# Built-ins skip class, use meta
> 
> # Explicit names search class + meta
> >>> class B(metaclass=A): 					# Data descriptors in meta used first
>         data = 'spam'
> >>> B[0] 						# Metaclass instance names: visible to class only
> 's'
> >>> B.__getitem__
> <bound method A.__getitem__ of <class '__main__.B'>>
> >>> I = B()
> >>> I.data, B.data 			# Normal inheritance names: visible to instance and class
> ('spam', 'spam')
> >>> I[0]
> TypeError: 'B' object does not support indexing
> ```

It's possible to define a \_\_getattr\_\_ on a metaclass too, but it can be used to process its instance classes only, not their normal instances -- as usual, it's not even acquired by a class's instances:
> ```python
> >>> class A(type):
>         def __getattr__(cls, name): 					# Acquired by class B getitem
>             return getattr(cls.data, name) 			# But not run same by built-ins
> 
> >>> class B(metaclass=A):
>         data = 'spam'
> 
> >>> B.upper()
> 'SPAM'
> >>> B.upper
> <built-in method upper of str object at 0x029E7420>
> >>> B.__getattr__
> <bound method A.__getattr__ of <class '__main__.B'>>
> >>> I = B()
> >>> I.upper
> AttributeError: 'B' object has no attribute 'upper'
> >>> I.__getattr__
> AttributeError: 'B' object has no attribute '__getattr__'
> ```

Moving the \_\_getattr\_\_ to a metaclass doesn't help with its built-in interception shortcomings, though. In the following continuation, explicit attributes are routed to the metaclass's \_\_getattr\_\_, but built-ins are not, despite that fact the indexing is routed to a metaclass's \_\_getitem\_\_ in the first example of the section -- strongly suggesting that new-style \_\_getattr\_\_ is a special case of a special case, and further recommending code simplicity that avoids dependence on such boundary cases:
> ```python
> >>> B.data = [1, 2, 3]
> >>> B.append(4) 				# Explicit normal names routed to meta's getattr
> >>> B.data
> [1, 2, 3, 4]
> >>> B.__getitem__(0) 			# Explicit special names routed to meta's gettarr
> 1
> >>> B[0] 						# But built-ins skip meta's gettatr too?!
> TypeError: 'A' object does not support indexing
> ```

As you can probably tell, metaclasses are interesting to explore, but it's easy to lose track of their big picture. In the interest of space, we'll omit additional fine points here. For the purposes of this chapter, it's more important to show why you'd care to use such a tool in the first place. Let's move on to some larger examples to sample the roles of metaclasses in action. As we’ll find, like so many tools in Python, metaclasses are first and foremost about easing maintenance work by eliminating redundancy.
