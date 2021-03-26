# Class Gotchas
We've reached the end of the primary OOP coverage in this book. After exceptions, we'll explore additional class-related examples and topics in the last part of the book, but that part mostly just gives expanded coverage to concepts introduced here. As usual, let's wrap up this part with the standard warnings about pitfalls to avoid.

Most class issues can be boiled down to namespace issues -- which makes sense, given that classes are just namespaces with a handful of extra tricks. Some of the items in this section are more like class usage pointers than problems, but even experienced class coders have been known to stumble on a few.

## Changing Class Attributes Can Have Side Effects
Theoretically speaking, classes (and class instances) are mutable objects. As with builtin lists and dictionaries, you can change them in place by assigning to their attributes -- and as with lists and dictionaries, this means that changing a class or instance object may impact multiple references to it.

That's usually what we want, and is how objects change their state in general, but awareness of this issue becomes especially critical when changing class attributes. Because all instances generated from a class share the class's namespace, any changes at the class level are reflected in all instances, unless they have their own versions of the changed class attributes.

Because classes, modules, and instances are all just objects with attribute namespaces, you can normally change their attributes at runtime by assignments. Consider the following class. Inside the class body, the assignment to the name a generates an attribute X.a, which lives in the class object at runtime and will be inherited by all of X's instances:
> ```python
> >>> class X:
>         a = 1 		# Class attribute
> >>> I = X()
> >>> I.a     			# Inherited by instance
> 1
> >>> X.a
> 1
> ```

So far, so good -- this is the normal case. But notice what happens when we change the class attribute dynamically outside the class statement: it also changes the attribute in every object that inherits from the class. Moreover, new instances created from the class during this session or program run also get the dynamically set value, regardless of what the class's source code says:
> ```python
> >>> X.a = 2 			# May change more than X
> >>> I.a 				# I changes too
> 2
> >>> J = X() 			# J inherits from X's runtime values
> >>> J.a 				# (but assigning to J.a changes a in J, not X or I)
> 2
> ```

Is this a useful feature or a dangerous trap? You be the judge. As we learned in Chapter 27, you can actually get work done by changing class attributes without ever making a single instance -- a technique that can simulate the use of "records" or "structs" in other languages. As a refresher, consider the following unusual but legal Python program:
> ```python
> class X: pass 			# Make a few attribute namespaces
> class Y: pass
> X.a = 1 					# Use class attributes as variables
> X.b = 2 					# No instances anywhere to be found
> X.c = 3
> Y.a = X.a + X.b + X.c
> for X.i in range(Y.a): print(X.i) 		# Prints 0..5
> ```

Here, the classes X and Y work like "fileless" modules -- namespaces for storing variables we don't want to clash. This is a perfectly legal Python programming trick, but it's less appropriate when applied to classes written by others; you can't always be sure that class attributes you change aren't critical to the class's internal behavior. If you're out to simulate a C struct, you may be better off changing instances than classes, as that way only one object is affected:
> ```python
> class Record: pass
> X = Record()
> X.name = 'bob'
> X.job = 'Pizza maker'
> ```

## Changing Mutable Class Attributes Can Have Side Effects, Too
This gotcha is really an extension of the prior. Because class attributes are shared by all instances, if a class attribute references a mutable object, changing that object in place from any instance impacts all instances at once:
> ```python
> >>> class C:
>         shared = [] 					# Class attribute
>         def __init__(self):
>             self.perobj = []			# Instance attribute
> 
> >>> x = C() 							# Two instances
> >>> y = C() 							# Implicitly share class attrs
> >>> y.shared, y.perobj
> ([], [])
> >>> x.shared.append('spam') 			# Impacts y's view too!
> >>> x.perobj.append('spam') 			# Impacts x's data only
> >>> x.shared, x.perobj
> (['spam'], ['spam'])
> >>> y.shared, y.perobj 				# y sees change made through x
> (['spam'], [])
> >>> C.shared 							# Stored on class and shared
> ['spam']
> ```

This effect is no different than many we've seen in this book already: mutable objects are shared by simple variables, globals are shared by functions, module-level objects are shared by multiple importers, and mutable function arguments are shared by the caller and the callee. All of these are cases of general behavior -- multiple references to a mutable object -- and all are impacted if the shared object is changed in place from any reference. Here, this occurs in class attributes shared by all instances via inheritance, but it's the same phenomenon at work. It may be made more subtle by the different behavior of assignments to instance attributes themselves:
> ```python
> x.shared.append('spam') 			# Changes shared object attached to class in place
> x.shared = 'spam' 				# Changed or creates instance attribute attached to x
> ```

But again, this is not a problem, it's just something to be aware of; shared mutable class attributes can have many valid uses in Python programs.

## Multiple Inheritance: Order Matters
This may be obvious by now, but it's worth underscoring: if you use multiple inheritance, the order in which superclasses are listed in the class statement header can be critical. Python always searches superclasses from left to right, according to their order in the header line.

For instance, in the multiple inheritance example we studied in Chapter 31, suppose that the Super class implemented a \_\_str\_\_ method, too:
> ```python
> class ListTree:
>     def __str__(self): ...
> class Super:
>     def __str__(self): ...
> class Sub(ListTree, Super): 		# Get ListTree's __str__ by listing it first
> x = Sub()  						# Inheritance searches ListTree before Super
> ```

Which class would we inherit it from -- ListTree or Super? As inheritance searches proceed from left to right, we would get the method from whichever class is listed first (leftmost) in Sub's class header. Presumably, we would list ListTree first because its whole purpose is its custom \_\_str\_\_ (indeed, we had to do this in Chapter 31 when mixing this class with a tkinter.Button that had a \_\_str\_\_ of its own).

But now suppose Super and ListTree have their own versions of other same-named attributes, too. If we want one name from Super and another from ListTree, the order in which we list them in the class header won't help -- we will have to override inheritance by manually assigning to the attribute name in the Sub class:
> ```python
> class ListTree:
>     def __str__(self): ...
>     def other(self): ...
> class Super:
>     def __str__(self): ...
>     def other(self): ...
> class Sub(ListTree, Super): 	# Get ListTree's __str__ by listing it first
>     other = Super.other 		# But explicitly pick Super's version of other
>     def __init__(self):
>         ...
> 
> x = Sub() 					# Inheritance searches Sub before ListTree/Super
> ```

Here, the assignment to other within the Sub class creates Sub.other -- a reference back to the Super.other object. Because it is lower in the tree, Sub.other effectively hides ListTree.other, the attribute that the inheritance search would normally find. Similarly, if we listed Super first in the class header to pick up its other, we would need to select ListTree's method explicitly:
> ```python
> class Sub(Super, ListTree): 			# Get Super's other by order
>     __str__ = Lister.__str__ 			# Explicitly pick Lister.__str__
> ```

Multiple inheritance is an advanced tool. Even if you understood the last paragraph, it's still a good idea to use it sparingly and carefully. Otherwise, the meaning of a name may come to depend on the order in which classes are mixed in an arbitrarily farremoved subclass. (For another example of the technique shown here in action, see the discussion of explicit conflict resolution in "The 'New-Style' Class Model", as well as the earlier super coverage.)

As a rule of thumb, multiple inheritance works best when your mix-in classes are as self-contained as possible -- because they may be used in a variety of contexts, they should not make assumptions about names related to other classes in a tree. The pseudoprivate \_\_X attributes feature we studied in Chapter 31 can help by localizing names that a class relies on owning and limiting the names that your mix-in classes add to the mix. In this example, for instance, if ListTree only means to export its custom \_\_str\_\_, it can name its other method \_\_other to avoid clashing with like-named classes in the tree.

## Scopes in Methods and Classes
When working out the meaning of names in class-based code, it helps to remember that classes introduce local scopes, just as functions do, and methods are simply further nested functions. In the following example, the generate function returns an instance of the nested Spam class. Within its code, the class name Spam is assigned in the generate function's local scope, and hence is visible to any further nested functions, including code inside method; it's the E in the "LEGB" scope lookup rule:
> ```python
> def generate():
>     class Spam: 					# Spam is a name in generate's local scope
>         count = 1
>         def method(self):
>             print(Spam.count) 			# Visible in generate's scope, per LEGB rule (E)
>     return Spam()
> generate().method()
> ```

This example works in Python since version 2.2 because the local scopes of all enclosing function defs are automatically visible to nested defs (including nested method defs, as in this example).

Even so, keep in mind that method defs cannot see the local scope of the enclosing class; they can see only the local scopes of enclosing defs. That's why methods must go through the self instance or the class name to reference methods and other attributes defined in the enclosing class statement. For example, code in the method must use self.count or Spam.count, not just count.

To avoid nesting, we could restructure this code such that the class Spam is defined at the top level of the module: the nested method function and the top-level generate will then both find Spam in their global scopes; it's not localized to a function's scope, but is still local to a single module:
> ```python
> def generate():
>     return Spam()
> class Spam: 				# Define at top level of module
>     count = 1
>     def method(self):
>         print(Spam.count) 		# Works: in global (enclosing module)
> generate().method()
> ```

In fact, this approach is recommended for all Python releases -- code tends to be simpler in general if you avoid nesting classes and functions. On the other hand, class nesting is useful in closure contexts, where the enclosing function's scope retains state used by the class or its methods. In the following, the nested method has access to its own scope, the enclosing function's scope (for label), the enclosing module's global scope, anything saved in the self instance by the class, and the class itself via its nonlocal name:
> ```python
> >>> def generate(label): 				# Returns a class instead of an instance
>         class Spam:
>             count = 1
>             def method(self):
>                 print("%s=%s" % (label, Spam.count))
>         return Spam
> 
> >>> aclass = generate('Gotchas')
> >>> I = aclass()
> >>> I.method()
> Gotchas=1
> ```

## Miscellaneous Class Gotchas
Here's a handful of additional class-related warnings, mostly as review.

### Choose per-instance or class storage wisely
On a similar note, be careful when you decide whether an attribute should be stored on a class or its instances: the former is shared by all instances, and the latter will differ per instance. This can be a crucial design issue in practice. In a GUI program, for instance, if you want information to be shared by all of the window class objects your application will create (e.g., the last directory used for a Save operation, or an already entered password), it must be stored as class-level data; if stored in the instance as self attributes, it will vary per window or be missing entirely when looked up by inheritance.

### You usually want to call superclass constructors
Remember that Python runs only one \_\_init\_\_ constructor method when an instance is made -- the lowest in the class inheritance tree. It does not automatically run the constructors of all superclasses higher up. Because constructors normally perform required startup work, you'll usually need to run a superclass constructor from a subclass constructor -- using a manual call through the superclass's name (or super), passing along whatever arguments are required -- unless you mean to replace the super's constructor altogether, or the superclass doesn't have or inherit a constructor at all.

### Delegation-based classes in 3.X: \_\_getattr\_\_ and built-ins
Another reminder: as described earlier in this chapter and elsewhere, classes that use the \_\_getattr\_\_ operator overloading method to delegate attribute fetches to wrapped objects may fail in Python 3.X (and 2.X when new-style classes are used) unless operator overloading methods are redefined in the wrapper class. The names of operator overloading methods implicitly fetched by built-in operations are not routed through generic attribute-interception methods. To work around this, you must redefine such methods in wrapper classes, either manually, with tools, or by definition in superclasses; we'll see how in Chapter 40.

## KISS Revisited: "Overwrapping-itis"
When used well, the code reuse features of OOP make it excel at cutting development time. Sometimes, though, OOP's abstraction potential can be abused to the point of making code difficult to understand. If classes are layered too deeply, code can become obscure; you may have to search through many classes to discover what an operation does.

For example, I once worked in a C++ shop with thousands of classes (some machinegenerated), and up to 15 levels of inheritance. Deciphering method calls in such a complex system was often a monumental task: multiple classes had to be consulted for even the most basic of operations. In fact, the logic of the system was so deeply wrapped that understanding a piece of code in some cases required days of wading through related files. This obviously isn't ideal for programmer productivity!

The most general rule of thumb of Python programming applies here, too: don't make things complicated unless they truly must be. Wrapping your code in multiple layers of classes to the point of incomprehensibility is always a bad idea. Abstraction is the basis of polymorphism and encapsulation, and it can be a very effective tool when used well.

However, you'll simplify debugging and aid maintainability if you make your class interfaces intuitive, avoid making your code overly abstract, and keep your class hierarchies short and flat unless there is a good reason to do otherwise. Remember: code you write is generally code that others must read. See Chapter 20 for more on KISS.
